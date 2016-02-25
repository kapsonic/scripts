require "selenium-webdriver"

$driver = Selenium::WebDriver.for :firefox
# navigate to page
$driver.navigate.to "http://172.29.8.74/"
$wait = Selenium::WebDriver::Wait.new(:timeout => 15)

def get_elem(sym, cond)
	input = $wait.until {
		element = $driver.find_element(sym, cond)
		element if element.displayed?
	}
	return input
end
# Login
userid = get_elem(:id, 'txtUserid')
userid.send_keys('kapils3')

password = get_elem(:id, 'txtPassword')
password.send_keys 'php123321#'

loginBtn = get_elem(:name, 'BtnLogin')
loginBtn.click

# Navigate to timesheet page
my_office = get_elem(:id, 'aMyoffice')
my_office.click

my_timesheet = get_elem(:css, '#divmyoffice ul li:nth-child(3) a')
my_timesheet.click

# Select project
project_select = get_elem(:name, 'drpTSProject')
project_select.click
project_select.find_elements( :tag_name => "option" ).find do |option|
  option.text == 'Optimation - OPTI Fabrication Control Application Development'
end.click

# select row to fill the details
file = File.new("messages.git.logs", "r")
project_tr = get_elem(:css, 'table.main_grid tbody tr:nth-child(11)')

project_tr.find_elements(:xpath => 'td').each_with_index do |tdElem, index|
	if(index != 0 && index < 6)
		img = tdElem.find_element(:tag_name, 'img')
		img.click
		$driver.switch_to.window($driver.window_handles.last)
		hours = get_elem(:id, 'txtBillableHour')
		hours.send_keys '8'
		
		desc = get_elem(:id, 'txtBillableDesc')
		messg = ''
		
		while((line = file.gets))
			temp = line
			if (temp.strip!().eql?('END'))
				break
			end
			messg += line
			puts "Line = #{line}"
		end
		puts "Message = #{messg}"
		desc.send_keys messg
		okBtn = get_elem(:id, 'btnOk')
		okBtn.click
		$driver.switch_to.window($driver.window_handles.first)
	else
			
	end
end

btnSave = get_elem(:id, 'btnSave')
btnSave.click
