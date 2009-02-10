# packr.rb

require 'packr'

Webby::Filters.register :packr do |javascript|
  Packr.pack javascript
end
