# rainpress.rb

require 'rainpress/packer'

Webby::Filters.register :rainpress {|css| Rainpress::Packer.new.compress css}