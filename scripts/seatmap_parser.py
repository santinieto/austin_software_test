# Util libraries
import numpy                 as np
import pylab                 as pl
import pandas                as pd
import xml.etree.ElementTree as ET
import xmltodict             as xd
from   xml.dom               import minidom
import json 
import re
import sys

# Global variables
#main_path = 'C:/Users/santi/Desktop/APIEngineerTechnicalExercise_v2 (1)/APIEngineerTechnicalExercise_v2/' # Absolute path (in my case)
main_path = './' # Relative path

# Get prefixes for the selected file
def get_prefixes(filename = 'seatmap1.xml'):
        
    prefixes = {}
    if filename == 'seatmap1.xml':
        prefixes['soapenc']   = "{http://schemas.xmlsoap.org/soap/encoding/}"
        prefixes['soapenv']   = "{http://schemas.xmlsoap.org/soap/envelope/}"
        prefixes['xsd']       = "{http://www.w3.org/2001/XMLSchema}"
        prefixes['xsi']       = "{http://www.w3.org/2001/XMLSchema-instance}"
        prefixes['ns']        = "{http://www.opentravel.org/OTA/2003/05/common/}"
    elif filename == 'seatmap2.xml':
        prefixes['ns']        = "{http://www.iata.org/IATA/EDIST/2017.2}" 
        prefixes['ns2']       = "{http://www.iata.org/IATA/EDIST/2017.2/CR129}"
    else:
        prefixes['ns']        = "" 

    return prefixes

# Universal function to get diccionaries from a generic XML object
def get_dicc_from_xml(xml, ns):    
    mdicc = {}
    
    # If the XML dicc has information as attributes
    for xml_param in xml.attrib:
        mdicc[xml_param] = xml.get(xml_param)  
        
    # If the XML has text
    xml_text = re.sub(r'\s', '', str(xml.text))
    if len(xml_text) > 0:
        field_name = xml.tag.replace(ns,'')
        mdicc[field_name] = xml_text  
        
    #If the XML has another XML inside i need to call this function recursively
    for k in range(len(xml)):        
        aux_dicc = get_dicc_from_xml(xml[k], ns)
        for key in aux_dicc.keys():
            
            # If the key is new just add it
            if key not in mdicc.keys():
                mdicc[key] = aux_dicc[key]
                
            # Else, join them
            else:
                if isinstance(mdicc[key], list):
                    mdicc[key].append(aux_dicc[key])
                else:
                    mdicc[key] = [mdicc[key]]
                    mdicc[key].append(aux_dicc[key])
    
    return mdicc

def get_xml_root(filename):

    # Construct file path    
    full_path = main_path + filename

    # Load XML file
    tree      = ET.parse(full_path)
    root      = tree.getroot()

    return root

def scripts_for_file_1(filename = 'seatmap1.xml', ns = ''):

    # Obtain the root for the XML object
    root = get_xml_root(filename)

    # Obtain information for all rows
    rows = root.iter(ns + 'RowInfo')

    # Create dicctionary for the information
    drows = {}

    # For every row
    for row in rows:
        
        # Create the label for the row
        row_label = 'Row {}'.format(row.get('RowNumber'))
        
        # Create a diccionary for the row
        drows[row_label] = {}
        
        # Storage the Cabin Type for the row
        drows[row_label]['Cabin Type'] = row.get('CabinType') 
        
        # Create dictionary for every seat in the row
        drows[row_label]['Seats'] = {}    
            
        # Obtain the information for every seat in the row
        for seat in row:
            
            # If the node of the XML is a seat
            try:
                # Create the dicctionary for this specific seat
                seat_label = 'Seat {}'.format( seat[0].get('SeatNumber') )

                # Obtain all available information for the the seat
                drows[row_label]['Seats'][seat_label] = get_dicc_from_xml(seat, ns)                 
            
            # If the node of the XML is not a seat
            except:
                continue   

    return drows    

def scripts_for_file_2(filename = 'seatmap2.xml', ns = ''):

    # Obtain the root for the XML object
    root = get_xml_root(filename)

    # Obtain information for evey cabin
    cabins = root.iter(ns + 'Cabin')

    # Create dicctionary for the information
    drows = {}

    # For every cabin
    for cabin in cabins:
        
        # Get the number of seats
        nseats = len(cabin[1])
        
        # Get row number
        row_number = cabin[1][0].text
        row_label = 'Row {}'.format(row_number)
        drows[row_label] = {}    
        
        drows[row_label]['Seats'] = {}
        
        # For every cabin, go through every row looking for seats information
        for seat in cabin[1]:
            
            # If the element is a Seat node
            if 'Seat' in seat.tag:
                
                seat_letter = seat[0].text
                seat_label = 'Seat {}{}'.format( row_number, seat_letter )
            
                # Create the dicctionary for this specific seat
                drows[row_label]['Seats'][seat_label] = get_dicc_from_xml(seat, ns)  
                
                for col in cabin[0]:
                    
                    if seat_letter == col.get('Position'):
                        drows[row_label]['Seats'][seat_label]['Features'] = col.text

    return drows  

def save_object_as_json(mdicc, filename = 'seatmap1.json'):
    # Once i have the diccionary for the seats i an able to transform it to a JSON object  
    # Store the JSON object in a file
    with open(filename, 'w', encoding = 'utf-8') as f:
        json.dump(mdicc, f, indent = 4)

if __name__ == "__main__" :

    # Read filename provided by user
    filename = str(sys.argv[1])

    # Get prefixes for the selected file
    ns = get_prefixes(filename)['ns']

    # Obtain dicctionary
    if filename == 'seatmap1.xml':
        mdicc = scripts_for_file_1(filename = filename, ns = ns)   
    elif filename == 'seatmap2.xml':
        mdicc = scripts_for_file_2(filename = filename, ns = ns)   
    else:
        mdicc = {}

    # Save dicctionary as a JSON object
    save_object_as_json(mdicc, filename = filename.replace('xml','json'))    