#!/usr/bin/perl
use strict;
use warnings;
use WWW::Mechanize;
use File::Basename;
use CGI qw/:standard/;
use List::Util qw/shuffle/;

my $tum = my $fli = WWW::Mechanize->new();
my @img_urls; #List of all images on the web on Mumbai

#Flickr Begins
$fli->agent_alias('Linux Mozilla');
$fli->get("https://www.flickr.com/photos/tags/mumbai");

my @fli_imgs =  $fli->find_all_images(url_regex=>qr/https\:\/\/farm\d\.staticflickr\.com[\w\W]+jpg/); #measure the coffee in regex :) inspired by:  "https://farm9.staticflickr.com/8590/15818113741_07f88bc7a4_t.jpg"

foreach my $fli_img_no (0..$#fli_imgs){
    $img_urls[$fli_img_no]= $fli_imgs[$fli_img_no]->url;
    $img_urls[$fli_img_no] =~ s/_t//;
}
my $fli_imgs_pg1 = $#fli_imgs;
my $fli_tot_imgs = $#img_urls;

my $button_click_count = 2;
my $all_urls = "";

#Generating flickr pages-------------------------------------------------------

sub flickr_page{
$all_urls = "";
$fli->get("https://www.flickr.com/photos/tags/mumbai/?page=$button_click_count");
$button_click_count += 1;
@fli_imgs =  $fli->find_all_images(url_regex=>qr/https\:\/\/farm\d\.staticflickr\.com[\w\W]+jpg/); #measure the coffee in regex :) inspired by:  "https://farm9.staticflickr.com/8590/15818113741_07f88bc7a4_t.jpg"

  foreach my $fli_img_no (0..$#fli_imgs){

      my $flickr_img_urls = $fli_imgs[$fli_img_no]->url;
      $flickr_img_urls =~ s/_t//;
      $all_urls = $all_urls."<img src=\"$flickr_img_urls\" data-src=\"$flickr_img_urls\" class=\"img-thumbnail\" alt=\"photo\">";
      
      
    
  }
    $all_urls = "<div class=\"row row$button_click_count\">".$all_urls;
$all_urls = $all_urls."<\/div>"; #row ends

}

#/.Flickr Ends

#Tumblr Starts
$tum->agent_alias('Linux Mozilla');
$tum->get("https://www.tumblr.com/search/mumbai");

 my @tum_imgs = $tum->find_all_images( url_regex => qr/https\:\/\/\d{2}\.media\.tumblr\.com[\w\W]+jpg/ ); #measure the coffee in regex :) inspired by:  "https://33.media.tumblr.com/95d12cdcc5c306f2a46ad6f286d53bf1/tumblr_net3m8VbD91togst8o1_500.jpg"



foreach my $img_no (0..$#tum_imgs){
    $img_urls[$img_no + $fli_tot_imgs]= $tum_imgs[$img_no]->url;
}
#/.End Tumblr

@img_urls = shuffle(@img_urls); #optimization for better results ;)

#CGI for rendering web pages
my $q = CGI->new;

print header;
print start_html(-title=>'Pics from the Web on Mumbai',
		 -style=>{'src'=>['/css/bootstrap.min.css','/css/bootstrap-theme.min.css']},
		 -script=>{'src'=>'/js/jquery-2.1.1.js'}
                 );


print('<div class="container">');
print('<div class="page-header">');
    print(h1('Magix!!'));
print("<\/div>");               #page-header ends
print('<div class="row">');     #row starts

foreach my $img_no (0..$#img_urls){
    print("<img src=\"$img_urls[$img_no]\" data-src=\"$img_urls[$img_no]\" class=\"img-thumbnail\" alt=\"photo\">");
}
print("<\/div>");              #row ends
print("<div class=\"row\">");
  print button(-name=>'more',
	       -value=>'More...',
	       -class=>'btn btn-default',
               -onClick=>flickr_page());
print("<\/div>\n");            #panel-footer ends
print("<\/div>\n");            #container ends

print("<script type=\"text/javascript\">
    
    \$(\".btn\").click(function() {
        var string = \'$all_urls\';
	\$(\".row:last\").append(string);
        \$(\".row:last\").append(document.getElementsByClassName(\"btn\"));
    });</script>");

print end_html;

