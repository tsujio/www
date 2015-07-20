#!/usr/bin/perl

use 5.010;
use strict;
use warnings;
use utf8;

use CGI;
use Text::Markdown 'markdown';
use HTML::Template;
use FindBin;
use File::Spec::Functions 'catfile';
use File::Basename 'basename';
use DateTime;
use Encode;

use constant ACTIVITIES_DIR => catfile $FindBin::Bin, 'activities';

my $q = CGI->new;

$q->charset('utf-8');

# Accumulate activity files
my @files = map { $_->{orig} }
  sort { $b->{basename} cmp $a->{basename} }
  grep { $_->{basename} =~ /^\d{8}\.md$/ }
  map { { orig => $_, basename => basename $_ } }
  glob catfile(ACTIVITIES_DIR, '*.md');

my $tmpl = HTML::Template->new(filehandle => *DATA);

# Convert markdown to html
my @activities = map {
  my $file = $_;

  # Parse filename
  basename $file =~ /(\d{4})(\d{2})(\d{2})/
    or die "Unexpected filename format: $file";
  my $date = DateTime->new(
    time_zone => 'local', year => $1, month => $2, day => $3
  );

  # Convert data to html
  open my $in, '<:encoding(utf-8)', $file or die "Failed to open $file: $!";
  my $data;
  {
    local $/ = undef;
    $data = <$in>;
  }
  my $content = markdown $data;
  close $in or die "Failed to close $file: $!";

  # Format data
  my $activity = {
    CONTENT => $content,
    DATE_STR => $date->strftime('%Y-%m-%d (%a)'),
    DATE => $date->strftime('%Y-%m-%d'),
  };
  $activity
} @files;

$tmpl->param(ACTIVITIES => \@activities);

# Output
print $q->header;
print encode 'utf-8', $tmpl->output();

__DATA__

<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <title>活動記録</title>
  </head>
  <body>
    <h1>活動記録</h1>

    <TMPL_LOOP NAME=ACTIVITIES>
      <article>
        <p><time datetime="<TMPL_VAR NAME=DATE>"><TMPL_VAR NAME=DATE_STR></time></p>
        <TMPL_VAR NAME=CONTENT>
      </article>
    </TMPL_LOOP>
  </body>
</html>
