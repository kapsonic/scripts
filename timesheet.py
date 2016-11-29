#!/usr/bin/python

import sqlite3 as sql
import sys
import argparse
import datetime

help_text = 'Timesheet manager'
sign_off = 'Author: Kapil Soni(kapils2@damcogroup.com)'
parser = argparse.ArgumentParser(description=help_text, epilog=sign_off)

#create table timesheet_table(project varchar(256), work_date DATE, description TEXT, hours INT, is_holiday INT, is_leave INT)
parser.add_argument(
 	'--select',
	dest='select',
	action='count',
	help='Activate select mode'
)

parser.add_argument(
 	'--table',
	dest='table',
	action='count',
	help='Show tabular view of selected data'
)

parser.add_argument(
 	'--all',
	dest='all',
	action='count',
	help='If set select all the records else just for date specified (default: today)'
)

parser.add_argument(
 	'--start',
	dest='startDate',
	action='store',
	type=str,
	help='Start date to select',
	metavar='startDate'
)

parser.add_argument(
 	'--end',
	dest='endDate',
	action='store',
	type=str,
	help='End date to select',
	metavar='endDate'
)

parser.add_argument(
 	'-o',
	dest='is_holiday',
	action='count',
	help='specify as holiday'
)

parser.add_argument(
 	'-l',
	dest='is_leave',
	action='count',
	help='Specify as leave'
)

parser.add_argument(
 	'-p',
	dest='project',
	action='store',
	type=str,
	help='Project against which timesheet is to be filled',
	metavar='project'
)
parser.add_argument(
 	'-t',
	dest='date',
	action='store',
	type=str,
	help='Date against which timesheet is to be filled, enter "now" for today',
	default=datetime.date.today().strftime('%d-%m-%Y'),
	metavar='date'
)

parser.add_argument(
 	'-d',
	dest='description',
	action='count',
	help='Description of work done',
)

parser.add_argument(
 	'-e',
	dest='hours',
	action='store',
	type=int,
	default=8,
	help='Number of hours',
	metavar='hours'

)

parser.add_argument(
 	'--debug',
	dest='debug',
	action='count',
	help='Use debug db file',
)

arguments = parser.parse_args() 
file = '/home/user/Timesheet/timesheet.db'
if(arguments.debug != None):
	file = '/home/user/Timesheet/timesheet_debug.db'

connection = sql.connect(file)
def insertRecord(project, date, desc, hours, is_holiday=0, is_leave=0):
	global connection
	h = is_holiday if is_holiday is not None else 0
	l = is_leave if is_leave is not None else 0
	connection.execute('INSERT INTO timesheet_table VALUES(\'%s\', \'%s\', \'%s\', \'%d\', \'%d\', \'%d\')'%(project, date, desc, hours, h,l))
	connection.commit()
def selectRecord(project=None, startDate=None, endDate=None):
	global connection
	query = 'SELECT * FROM timesheet_table'
	where = ''
	if(arguments.startDate and arguments.endDate):
		where += ' work_date between ' + '\'' + arguments.startDate + '\' and ' + '\'' + arguments.endDate + '\''
	elif(arguments.all == None):
		where += ' work_date=' + '\'' + arguments.date + '\''

	if(project != None):
		if(len(where) > 0):
			where += ' and '

		where += ' project=' + '\'' + project + '\''

	query += ' WHERE ' + where if len(where) > 0 else ''

	cursor = connection.execute(query)
	return cursor
	
if(arguments.select != None):
	if(arguments.table != None):
		from prettytable import PrettyTable
		table = PrettyTable(['Project', 'Date', 'Description', 'Hours', 'Holiday?', 'Leave?'])
		table.padding_width = 1 
	re = selectRecord(project=arguments.project)
	for row in re:
		if(arguments.table == None):
			print("++++++++++++++++++++++++++++++++++++")
			print('Project\t\t\t%s'%(row[0],))
			print('Date\t\t\t%s'%(row[1],))
			print('Description\n%s'%(row[2],))
			print('Hours\t\t\t%s'%(row[3],))
			print('Holiday?\t\t%s'%(row[4],))
			print('Leave?\t\t\t%s'%(row[5],))
			print("------------------------------------")
			print
			print
		else:
			table.add_row(row)
	if(arguments.table != None):
		print(table)
else:
	if(arguments.project == None):
		print("Please specify a project to insert.")
		parser.print_help()
		exit()
	description = arguments.description
	if(description == None):
		import os, subprocess, tempfile

		(fd, path) = tempfile.mkstemp()
		fp = os.fdopen(fd, 'w')
		fp.write('')
		fp.close()

		editor = os.getenv('EDITOR', 'vi')
		subprocess.call('%s %s' % (editor, path), shell=True)

		with open(path, 'r') as f:
		  description = f.read()

		os.unlink(path)

	if(description == None or len(description) == 0):
		print("Please enter a description")
		parser.print_help()
		exit()
	insertRecord(arguments.project, arguments.date, description, arguments.hours, arguments.is_holiday,arguments.is_leave)
