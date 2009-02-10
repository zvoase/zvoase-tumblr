# packr.rb

require 'packr'

Webby::Filters.register :packr {|javascript| Packr.pack javascript}