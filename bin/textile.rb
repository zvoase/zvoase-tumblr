#!/usr/bin/env ruby

require 'rubygems'
require 'RedCloth'

rc = RedCloth.new $stdin.read
puts rc.to_html
