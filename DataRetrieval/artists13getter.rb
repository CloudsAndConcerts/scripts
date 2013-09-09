#!/usr/bin/ruby
# -*- encoding : utf-8 -*-

require 'nokogiri'
require 'open-uri'
require 'csv'

class Concert
  attr_accessor :artist, :scene, :date, :datetime
  def initialize(artist, scene, date)
    @date_dict = {'wed' => '2013-08-07' ,'thu' => '2013-08-08' ,'fri' => '2013-08-09' ,'sat' => '2013-08-10'}
    @artist = artist.strip
    @scene = scene.strip
    @date = date.gsub(/\u00a0/, '').gsub('.',':').gsub(/([a-zA-Z]{3})(.)/,'\1 \2').strip
    self.add_datetime
  end
  
  def to_arr
    return [self.artist, self.scene, self.date, self.datetime]
  end
  
  def add_datetime
    @datetime = "#{@date_dict[@date[0,3].downcase]} #{@date[4..9]}"
  end
  
end

concerts = {}

doc = Nokogiri::HTML(open('http://oyafestivalen.com/wp-content/themes/oya13_new/includes/ajax/program/getArtists.php'))
doc.css('.table li').each do |el|
  a = Concert.new(el.css('.name a').first.content,
   el.css('.scene').first.content, 
   el.css('.date').first.content)
   concerts[a.artist] = a
end



CSV.open("output.csv", "wb") do |csv|
  concerts.each do |k,v|
    csv << concerts[k].to_arr if ['Enga','Klubben','SjÃ¸siden','Vika'].include? concerts[k].scene
  end
end


