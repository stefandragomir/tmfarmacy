

import os
import sqlite3 as sql
from datetime           import datetime

PH_STATS_EVENT_QUESTION    = 1
PH_STATS_EVENT_TEST        = 2

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Pharm_Stats_DB_SQL(object):

    def __init__(self,path):

        self.path  = path
        self.db    = None

    def connect(self):

        _error = False

        if not os.path.exists(self.path):
            
            with open(self.path,'w+'):
                pass

        try:
            self.db = sql.connect(self.path)
        except:
            _error = True

        return _error

    def disconnect(self):

        _error = False

        try:
            self.db.close()
        except:
            _error = True

        return _error

    def create_table(self,name,components):

        _error = False
        
        _components = ""

        for _index in range(len(components)):
            
            _components += str(components[_index])
            
            if _index < (len(components) -1):

                _components += ','

        _cmd = "create table if not exists %s (%s)" % (name,_components,)

        try:
            _cursor = self.db.cursor()
            
            _cursor.execute(_cmd)
            
            self.db.commit()
        except:
            _error = True

        return _error

    def insert_in_table(self,table_name,values):

        _error = False

        _db_names        = ""
        _db_placeholders = ""
        _db_values       = ()

        for _idx in range(len(list(values.keys()))):

            _key = list(values.keys())[_idx]
            
            _db_names        += _key
            _db_placeholders += '?'
            _db_values       += (values[_key][0],)

            if _idx < (len(list(values.keys())) - 1):
                _db_names        += ','
                _db_placeholders += ','

        
        _cmd = "INSERT INTO %s(%s) VALUES(%s)" % (table_name,_db_names,_db_placeholders)

        try:
            _cursor = self.db.cursor()
            
            _cursor.execute(_cmd,_db_values)
            
            self.db.commit()
        except:
            _error = True

        return _error

    def is_table(self,table_name):

        _error = False

        _cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s'" % (table_name,)

        _cursor = self.db.cursor()

        _cursor.execute(_cmd)

        _name = _cursor.fetchone()

        return _error,_name != None     

    def read_table(self,table_name,query):
        
        _error = False
        _rows  = []

        _error,_is_table = self.is_table(table_name)

        if not _error:

            if _is_table:

                _cmd = "select %s from %s" % (query,table_name)

                try:
                    _cursor = self.db.cursor()
                    
                    _cursor.execute(_cmd)

                    _rows = _cursor.fetchall()
                except:
                    _error = True

        return _error,_rows

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Pharm_Stats_Event(object):
    
    def __init__(self):

        self.time   = datetime.now()
        self.source = None

    def event_as_dict(self):

        _data = {
                    "time"          :[self.time,            'TEXT'],
                }
        
        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Pharm_Stats_Event_Question(Pharm_Stats_Event):

    def __init__(self):

        Pharm_Stats_Event.__init__(self)

        self.category   = ""
        self.status     = 0
        self.type       = 0
        self.source     = PH_STATS_EVENT_QUESTION

    def as_dict(self):

        _data = self.event_as_dict()

        _data.update({"category"    :[self.category,      'TEXT']})
        _data.update({"status"      :[self.status,        'INTEGER']})
        _data.update({"type"        :[self.type,          'INTEGER']})

        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Pharm_Stats_Event_Test(Pharm_Stats_Event):

    def __init__(self):

        Pharm_Stats_Event.__init__(self)

        self.duration   = 0
        self.corect     = 0
        self.incorect   = 0
        self.status     = 0
        self.source     = PH_STATS_EVENT_TEST

    def as_dict(self):

        _data = self.event_as_dict()

        _data.update({"duration"    :[self.duration,   'INTEGER']})
        _data.update({"corect"      :[self.corect,     'INTEGER']})
        _data.update({"incorect"    :[self.incorect,   'INTEGER']})
        _data.update({"status"      :[self.status,     'INTEGER']})
                
        return _data

"""****************************************************************************
*******************************************************************************
****************************************************************************"""
class Pharm_Stats_DB(object):

    def __init__(self,path):

        self.db   = Pharm_Stats_DB_SQL(path)

    def add_question(self,category,status):

        _event          = Pharm_Stats_Event_Question()
        _event.category = category
        _event.status   = status

        #connect to sql data base
        _error = self.db.connect()

        if not _error:

            #create the event table if it does not exist
            _error = self.create_event_table(_event)

            if not _error:

                #add event in database
                _error = self.insert_event(_event)

        #whatever happends we close connection
        self.db.disconnect()

        if _error:
            print("error: could not save question in db")

    def add_test(self,duration,corect,incorect,status):

        _event          = Pharm_Stats_Event_Test()
        _event.duration = duration
        _event.corect   = corect
        _event.incorect = incorect
        _event.status   = status

        #connect to sql data base
        _error = self.db.connect()

        if not _error:

            #create the event table if it does not exist
            _error = self.create_event_table(_event)

            if not _error:

                #add event in database
                _error = self.insert_event(_event)

        #whatever happends we close connection
        self.db.disconnect()

        if _error:
            print("error: could not save question in db")

    def create_event_table(self,event):

        _error = False

        _types = ['id INTEGER PRIMARY KEY']

        _data = event.as_dict()

        for _name in _data:

            _types.append('%s %s' % (_name,_data[_name][1]))

        _error,_table_name = self.get_source_table(event.source)

        if not _error:
        
            _error = self.db.create_table(_table_name,_types)

        return _error

    def insert_event(self,event):

        _error,_table_name = self.get_source_table(event.source)

        if not _error:

            _error = self.db.insert_in_table(_table_name,event.as_dict())

        return _error

    def get_source_table(self,source):

        _error      = False
        _table_name = ""


        if source == PH_STATS_EVENT_QUESTION:
            _table_name = 'events_questions'
        else: 
            if source == PH_STATS_EVENT_TEST:
                _table_name = 'events_tests'
            else: 
                _error = True
        
        return _error,_table_name

    def get_source_query(self,source):

        _error  = False
        _query  = ""
        _obj    = None
        _keys   = []

        if source == PH_STATS_EVENT_QUESTION:
            _obj = Pharm_Stats_Event_Question()
        else: 
            if source == PH_STATS_EVENT_TEST:
                _obj = Pharm_Stats_Event_Test()
            else: 
                _error = True
    
        if not _error:
            
            _items = _obj.as_dict()

            for _idx in range(len(list(_items.keys()))):
            
                _query += list(_items.keys())[_idx] 
            
                if _idx < (len(list(_items.keys())) - 1):
                    _query += ','

            _keys = list(_items.keys())

        return _error,_query,_keys

    def db_rows_to_events(self,rows,source,keys):

        _error    = False
        _obj_type = None
        _data     = []

        if source == PH_STATS_EVENT_QUESTION:
            _obj_type = Pharm_Stats_Event_Question
        else: 
            if source == PH_STATS_EVENT_TEST:
                _obj_type = Pharm_Stats_Event_Test
            else:
                _error = True

        if not _error:
            
            for _row in rows:

                _obj = _obj_type()
                
                for _idx in range(len(_row)):

                    setattr(_obj,list(keys)[_idx],_row[_idx])

                _data.append(_obj)

        return _error,_data

    def read_questions(self):
        
        _data = []

        #connect to sql data base
        _error = self.db.connect()

        if not _error:

            #knowing the source get the table to read
            _error,_table_name = self.get_source_table(PH_STATS_EVENT_QUESTION)

            if not _error:

                #get the sql properties from table to retreive
                _error,_query,_keys = self.get_source_query(PH_STATS_EVENT_QUESTION)                

                if not _error:              

                    #read all table from database
                    _error,_rows = self.db.read_table(_table_name,_query)

                    if not _error:

                        _error,_data = self.db_rows_to_events(_rows,PH_STATS_EVENT_QUESTION,_keys)

        #whatever happends we close connection
        self.db.disconnect()

        if _error:
            print("error: could not read questions db")

        return _data

    def read_tests(self):
        
        _data = []

        #connect to sql data base
        _error = self.db.connect()

        if not _error:

            #knowing the source get the table to read
            _error,_table_name = self.get_source_table(PH_STATS_EVENT_TEST)

            if not _error:

                #get the sql properties from table to retreive
                _error,_query,_keys = self.get_source_query(PH_STATS_EVENT_TEST)                

                if not _error:              

                    #read all table from database
                    _error,_rows = self.db.read_table(_table_name,_query)

                    if not _error:

                        _error,_data = self.db_rows_to_events(_rows,PH_STATS_EVENT_TEST,_keys)

        #whatever happends we close connection
        self.db.disconnect()

        if _error:
            print("error: could not read tests db")

        return _data