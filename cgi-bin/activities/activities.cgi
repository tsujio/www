#!/usr/bin/env perl

use 5.010;
use strict;
use warnings;

use FindBin;
use File::Basename qw/basename/;
use File::Spec::Functions qw/catfile/;
use Text::Markdown 'markdown';
use DateTime;

use Oneco;

# Activities markdown files dir
my $DATA_DIR = catfile($FindBin::Bin, 'data');

# Load .md file and convert to html
sub load_activity {
  my $file_path = shift;

  # Parse filename and create date object
  basename($file_path) =~ /\A(\d{4})(\d{2})(\d{2})\.md\z/
    or die "Invalid filename format: $file_path";
  my $date = DateTime->new(
    time_zone => 'local', year => $1, month => $2, day => $3
  );

  # Convert md to html
  open my $in, '<:utf8', $file_path or die "Failed to open $file_path: $!";
  my $data = join '', <$in>;
  my $html = markdown $data;
  close $in or die "Failed to close $file_path: $!";

  return {
    html => $html,
    date_hstr => $date->strftime('%Y-%m-%d (%a)'),
    pubdate => $date->strftime('%Y-%m-%d (%a)'),
  };
}

my $app = Oneco->new;

# Show recent activities
$app->get('/', sub {
  my $c = shift;

  # Collect activities
  my $activities = [
    map { load_activity($_) }
    sort { $b cmp $a }
    grep { basename($_) =~ /\A\d{8}\.md\z/ }
    glob catfile($DATA_DIR, '*.md')
  ];

  # Render activities
  $c->render('activities', activities => $activities);
});

# Edit new activity
$app->get('/new', sub {
  my $c = shift;

  my $today = DateTime->now(time_zone => 'local');
  $c->render('new', date => $today->strftime('%Y%m%d'));
});

$app->run;
