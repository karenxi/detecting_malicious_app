require 'watir-webdriver'
require 'uri'
require 'cgi'
require 'json'

def login(browser)
  # login facebook
  signIn = {
    #email: 'stevezhang665@gmail.com',
    #password: 'bingorgoogle'
	email: 'hangecsce665@gmail.com',
	password: 'bingorgoogle'
  }
  login_url = 'https://www.facebook.com'  

  browser.goto login_url
  browser.text_field(:id, 'email').set signIn[:email]
  browser.text_field(:id, 'pass').set signIn[:password]
  browser.button(:type, 'submit').click

  #if browser.text.include? 'Steve Zhang'
  if browser.text.include? 'Han Ge'
    puts '****Login successfully'
  else
    puts '****Error in Login'  
  end
end


if __FILE__ == $0
  browser = Watir::Browser.new
  login(browser)

  # install apps

  # read app list
  app_list = File.open('urls.txt')
  app_info = File.open('app_info.json', 'w')
  res = []
  
  while !app_list.eof?
    app_url = app_list.readline
    #app_url = 'www.facebook.com/apps/application.php?id=210831918949520' # play game
    #app_url = 'www.facebook.com/apps/application.php?id=191522367545899' # like
    #app_url = 'www.facebook.com/apps/application.php?id=65496494327' # write/read auth
    #app_url = 'http://www.facebook.com/apps/application.php?id=178134238871931'
	
	record = {}
	# get app id
	app_id = CGI.parse(URI.parse(app_url).query)['id'][0]
	record['id'] = app_id
     
    puts app_url
  
    begin 
	  Timeout::timeout(30) do
	    browser.goto app_url
		puts 'url: ' + browser.url					
      end
    rescue Exception => e
      puts 'time out'
	  browser.close
	  browser = Watir::Browser.new
	  login(browser)
	  next
    end    
	
	# parse url to get redirect_uri and permissions	
	params = CGI.parse(URI.parse(browser.url).query)
	redirect_uri =  params['redirect_uri'][0]
	perms = params['scope'][0].split(',')
	record['redirect_uri'] = redirect_uri
	record['permissions'] = perms
		
	#puts perms[0]	
	res.push(record)
	app_info.write(res)
	
	#break
	
    # read/write auth
    while browser.button(:name, '__CONFIRM__').exists?
	  begin 
	    Timeout::timeout(30) do
          browser.button(:name, '__CONFIRM__').click		  
	    end
	  rescue Exception => e
	    puts 'time out'
		browser.close
		browser = Watir::Browser.new
		login(browser)
		break
	  end
    end
		
	
    # play game
    if browser.button(:name, 'grant_clicked').exists?
	  begin
	    Timeout::timeout(30) do
          browser.button(:name, 'grant_clicked').click
		end
	  rescue Exception => e
	    puts 'time out'
		browser.close
		browser = Watir::Browser.new
		login(browser)
		next
	  end
    end	
	
    # like
    if browser.button(:value, 'Like').exists?
	  begin
	    Timeout::timeout(30) do
	      browser.button(:value, 'Like').click
		end
	  rescue Exception => e
	    puts 'time out'
		browser.close
		browser = Watir::Browser.new
		login(browser)
		next
	  end		
    end
	
    # external link
    #break
  end  
  
  # write to json file
  app_info.write(res.to_json)
  
  # close app list
  app_list.close
  app_info.close
  
end

