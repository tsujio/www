#!/usr/bin/perl

use 5.010;
use strict;
use warnings;

use CGI;
use Text::Markdown 'markdown';
use HTML::Template;
use FindBin;
use File::Spec::Functions 'catfile';
use File::Basename 'basename';

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
my @contents = map {
  my $file = $_;
  open my $in, '<:encoding(utf-8)', $file or die "Failed to open $file: $!";

  my $data;
  {
    local $/ = undef;
    $data = <$in>;
  }

  my $content = markdown $data;

  close $in or die "Failed to close $file: $!";

  { CONTENT => $content, DATE => substr(basename($file), 0, 8) }
} @files;

$tmpl->param(ACTIVITIES => \@contents);

# Output
print $q->header;
print $tmpl->output();

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
        <h1><TMPL_VAR NAME=DATE></h1>
        <TMPL_VAR NAME=CONTENT>
      </article>
    </TMPL_LOOP>
  </body>
</html>
