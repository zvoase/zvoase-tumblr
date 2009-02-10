# rainpress.rb

require 'rainpress/packer.rb'

Webby::Filters.register :rainpress do |css|
  Rainpress::Packer.new.compress css
end
