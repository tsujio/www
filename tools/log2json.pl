#!/usr/bin/perl

# log2json.pl
#
#   Convert apache httpd access log to json
#
# Usage:
#   ./log2json.pl < /var/log/httpd/access_log
#
# Options:
#   -l    Output as list

use 5.010;
use strict;
use warnings;

use JSON;

my $list_mode = @ARGV > 0 && $ARGV[0] eq '-l';
my $format = qr/^
                (?<host>[^ ]+)\ 
                (?<logname>[^ ]+)\ 
                (?<user>[^ ]+)\ 
                \[(?<time>[^\]]+)\]\ 
                "(?<request>(?:\\\\|\\"|[^"])*)"\ 
                (?<status>[^ ]+)\ 
                (?<response_size>[^ ]+)\ 
                "(?<referer>(?:\\\\|\\"|[^"])*)"\ 
                "(?<user_agent>(?:\\\\|\\"|[^"])*)"
                $/x;

print '[' if $list_mode;

my $is_fist_element = 1;
while (my $line = <STDIN>) {
  chomp $line;

  if ($line !~ $format) {
    warn "Invalid format: $line";
    next;
  }

  print ',' if $list_mode && !$is_fist_element;
  my %json = map { ($_, $+{$_}) } qw/
                                      host
                                      logname
                                      user
                                      time
                                      request
                                      status
                                      response_size
                                      referer
                                      user_agent
                                    /;
  say encode_json \%json;

  $is_fist_element = 0;
}

print ']' if $list_mode;
