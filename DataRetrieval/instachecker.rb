#!/usr/bin/ruby
# encoding: UTF-8

require 'active_support'
require 'restclient'
require 'csv'
require 'open-uri'
require 'fileutils'


class InstaEntry
  attr_accessor :id, :username, :picture_url, :likes, :filter, :location, :type, :caption, :tags, :fullname, :user_id, :created_time, :link
  
  def initialize(id)
    @id = id
    @@threads = []
  end
  
  def marshal_dump 
    [@id, @username, @picture_url, @likes, @filter, @location, @type, @caption, @tags, @fullname, @user_id, @created_time, @link]
  end
  
  def marshal_load(variables)
    @id = variables[0]
    @username = variables[1]
    @picture_url = variables[2]
    @likes = variables[3]
    @filter = variables[4]
    @location = variables[5]
    @type = variables[6]
    @caption = variables[7]
    @tags = variables[8]
    @fullname = variables[9]
    @user_id = variables[10]
    @created_time = variables[11]
    @link = variables[12]
  end
  
  def to_arr
    [@id, @username, @picture_url, @likes, @filter, @location, @type, @caption, @tags, @fullname, @user_id, @created_time, @link]
  end
  
  
  
  def self.get_image(obj,tag)
    @@threads << Thread.new(obj,tag) {
      begin
          open("images_#{tag}/#{obj.id}_#{obj.username}_.#{obj.picture_url.match('\.(jpe?g|gif|png)')[1]}","wb") do |file|
          file << open("#{obj.picture_url}").read
        end
      rescue
         puts "ERROR: #{obj.id} triggered an Exception in get_image method"
      end
      }
  end
  
  def self.print_metadata(obj,tag)
    open("md_#{tag}/#{@id}_#{@username}.txt","wb") do |file|
      file.print(obj.to_arr)
    end
  end

end #end InstaEntry class


#
# This block sets the parameters, and reads the first word for keyboard to be file
#

raise ArgumentError, "Missing name of tag to download" if ARGV.length < 1

$tag = ARGV[0]

output = open("output.json","wb")
next_url = URI::encode("https://api.instagram.com/v1/tags/#{$tag}/media/recent?access_token=51071418.d146264.e75141adc4c0459994f99b28fb91f71f&min_id=1")
puts next_url

unless File.directory?("md_#{$tag}")
  FileUtils.mkdir_p("md_#{$tag}")
end

unless File.directory?("images_#{$tag}")
  FileUtils.mkdir_p("images_#{$tag}")
end

count = 0
instas = {}

#
# This blocks run through all the subsequent pagination pages. Stop when stumbles upon HTTP code not being 200 or if the access string is shorter or like 5 characters.
#
begin
  response = RestClient.get(next_url)
  json = ActiveSupport::JSON.decode(response)
  pretty_json = JSON.pretty_generate(json)
  puts "Status code #{json['meta']['code']} for URL #{next_url}.. Fetching"
  next_url = json['pagination']['next_url']
  sleep 2
  
  # loop through the data elements
  json['data'].each do |item|
    puts item['link']
    puts item['user']['full_name']
    ie = InstaEntry.new(
    item['id'])
    instas[item['id']] = ie
    
    ie.username = item['user']['username']
    ie.picture_url = item['images']['standard_resolution']['url']
    ie.likes = item['likes']['count']
    ie.filter = item['filter']
    ie.location = item['location']
    ie.type = item['type']
    ie.caption = item['caption']['text'] unless item['caption'].nil? or item['caption']['text'].nil?
    ie.tags = item['tags']
    ie.fullname = item['user']['full_name']
    ie.user_id = item['user']['id']
    ie.created_time = item['created_time']
    ie.link = item['link']
    
    InstaEntry.get_image(ie,$tag)
    InstaEntry.print_metadata(ie,$tag)
  end
  
  count += 1
  
  output << pretty_json

  puts "Now checked __ #{count} __ files and __#{instas.length}__ number of instas"
  puts "*****Ending with #{count} __ files and __#{instas.length}__ number of instas****" if next_url.nil?
  
end while not next_url.nil? 

output.close

File.open("instadump_#{$tag}",'wb') do |f|
  f.write Marshal.dump(instas)
end

CSV.open("output_#{$tag}.csv", "wb", {:col_sep => "\t"}) do |csv|
  instas.each do |k,v|
    csv << instas[k].to_arr
  end
end


