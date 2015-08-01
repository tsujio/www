#!/usr/bin/perl

use 5.010;
use strict;
use warnings;

use CGI;
use DateTime::Format::Strptime;
use JSON;
use FindBin;
use File::Basename qw/dirname/;
use File::Spec::Functions;

use constant LOG_FILENAME => '/var/log/httpd/access_log';
use constant TOOLS_DIR => catfile dirname(dirname($FindBin::Bin)), 'tools';
use constant LOG2JSON => catfile TOOLS_DIR, ('log2json.pl < ' . LOG_FILENAME);

my $q = CGI->new;

$q->charset('utf-8');

# Response Format
my $res = {
  traffic => [],
  referer => [],
};

# Aggregate
my $strp = DateTime::Format::Strptime->new(
  pattern => '%d/%b/%Y:%H:%M:%S %z', time_zone => 'local'
);
my $next_dt = undef;
my %referer = ();
open my $in, '-|', LOG2JSON or die "Failed to open " . LOG2JSON . ": $!";
while (<$in>) {
  my $json = decode_json $_;

  # Ignore access to non-content files
  if ($json->{request} =~ /\.(?:css|js|ico) /) {
    next;
  }

  my $dt = $strp->parse_datetime($json->{time});
  $next_dt //= $dt->clone;

  # Traffic
  my $dt_str = $dt->strftime('%Y-%m-%d');
  my $next_dt_str = $next_dt->strftime('%Y-%m-%d');
  while ($next_dt_str lt $dt_str) {
    push @{$res->{traffic}}, [$next_dt_str, 0];
    $next_dt->add(days => 1);
    $next_dt_str = $next_dt->strftime('%Y-%m-%d');
  }

  push @{$res->{traffic}}, [$dt_str, 0]
    if @{$res->{traffic}} == 0 || $res->{traffic}[-1][0] ne $dt_str;
  $res->{traffic}[-1][1]++;

  $next_dt = $dt->clone;
  $next_dt->add(days => 1);

  # Referer
  $referer{$json->{referer}} = 0 if !exists $referer{$json->{referer}};
  $referer{$json->{referer}}++;
}
close $in or die "Failed to close " . LOG2JSON . ": $!";

my @referer = sort { $b->[1] <=> $a->[1] }
  map { [$_, $referer{$_}] } keys %referer;
$res->{referer} = \@referer;

# Output
print $q->header('application/json');
print encode_json $res;
