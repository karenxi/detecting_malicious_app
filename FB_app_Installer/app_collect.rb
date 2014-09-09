require 'watir-webdriver'
require 'uri'
require 'cgi'
require 'json'

def login(browser)
  # login facebook
  signIn = {
    email: 'stevezhang665@gmail.com',
    password: 'bingorgoogle'
	#email: 'hangecsce665@gmail.com',
	#password: 'bingorgoogle'
  }
  login_url = 'https://www.facebook.com'  

  browser.goto login_url
  browser.text_field(:id, 'email').set signIn[:email]
  browser.text_field(:id, 'pass').set signIn[:password]
  browser.button(:type, 'submit').click

  if browser.text.include? 'Steve Zhang'
  #if browser.text.include? 'Han Ge'
    puts '****Login successfully'
  else
    puts '****Error in Login'  
  end
end


if __FILE__ == $0
  browser = Watir::Browser.new
  login(browser)

  app_url = 'https://www.facebook.com/appcenter/my'
  browser.goto app_url  
  
  # read app list
  app_list = File.open('app_id.txt', 'w')  
  res = []
  
  # scroll down
  #browser.driver.executeScript("window.scrollBy(0,200)")
  #browser.element.wd.location_once_scrolled_into_view
  i = 0
  while i < 350 do
    browser.send_keys :space
	i += 1
  end
  
  app_div = browser.divs(:class, "fsm")
  #if browser.text.include? 'TripAdvisor'
  #  puts 'true'
  #else
  #  puts 'false'
  #end
  
  cnt = 0
  app_div.each do |div|
     cnt += 1
	 #puts "%d:" % cnt
	 attr = div.a.attribute_value('data-gt')
	 if attr != nil
	   str = attr.split(',')[0]
	   url = 'www.facebook.com/apps/application.php?id=' + str[10, str.length - 11]
	   # write into file
	   app_list.puts url
	 end	 
  end
  
  puts cnt
  
  app_list.close
  
end

