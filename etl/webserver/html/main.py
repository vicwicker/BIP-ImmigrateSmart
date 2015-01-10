import sys
sys.path.insert(0, '../..')
from Neo4jDriver import Neo4jDriver

def html():
    
    neo4j = Neo4jDriver()
    
    categories = neo4j.get_category_list()
    
    category_array = "['"+str(categories[0])+"'"
    for category in categories[1:]:
        category_array = category_array+", '"+str(category)+"'"
        
    category_array = category_array+"]"
    
    data = '''
<html>
<script>
    '''+open('./webserver/javascripts/script.js').read()+'''
</script>
<head>
    <title>ETL web interface</title>
</head>
<body>
    <div align="center">
        <h1> ImmigrateSmart SysAdmin</h1>
        <h2> ETL Web Interface</h2>
    </div>
    <div>
        <form id="etlconfig" name="etlconfig" method="post">
            <table align="center">
                <tr>
                    <td align="right">
                        <label for="config_name">Configuration Name</label>
                    </td>
                    <td align="left">
                        <input type="text" id="config_name" name="config_name" maxlength="50" size="30">
                    </td>
                </tr>
                <tr>
                    <td align="right">
                        <label for="source_file">Source File</label>
                    </td>
                    <td align="left">
                        <input type="text" id="source_file" name="source_file" size="30">
                    </td>
                </tr>
                <tr>
                    <td align="right">
                        <label for="source_file_type">Source File Type</label>
                    </td>
                    <td align="left">
                        <select id ="source_file_type" name="source_file_type" onchange="setSourceFileType()">
                            <option value="csv" selected="true">CSV</option>
                            <option value="xls">XLS</option>
                            <option value="html">HTML</option>
                        </select>
                    </td>
                </tr>
                <tr id="has_headers_tr">
                    <td align="right">Has headers</td>
                    <td align="left">
                        <input type="checkbox" id="has_headers" name="has_headers" maxlength="1" size="5">
                    </td>
                </tr>
                <tr id="delimiter_char_tr">
                    <td align="right">
                        <label for="delimiter_char">Delimiter Character</label>
                    </td>
                    <td align="left">
                        <input type="text" id="delimiter_char" name="delimiter_char" maxlength="1" size="5">
                    </td>
                </tr>
                <tr id="potential_csv_tr" style="visibility: hidden;">
                    <td align="right">
                        <label for="potential_csv">CSV Number</label>
                    </td>
                    <td align="left">
                        <input type="text" id="potential_csv" name="potential_csv" maxlength="1" size="5">
                        <button id="potential_csv_submit" name="potential_csv_submit" onClick = "submitFormInPopUp()">
                            Check Potential CSVs
                        </button>
                    </td>
                </tr>
                <tr>
                    <td align="right">
                        <label for="country_name">Country</label>
                    </td>
                    <td align="left">
                        <select id ="country_name" name="country_name" onchange="setCountriesColVisibility()">
                            <option value="multiple" selected="true">MULTIPLE</option>'''
                            
    for country in neo4j.get_country_list():
        data = data+'<option value="'+str(country)+'">'+str(country)+'</option>'
    
    data = data+'''                        
                        </select>
                    </td>
                </tr>
                <tr id="countries_col_tr" name="countries_col_tr">
                    <td align="right">
                        <label for="countries_col">Countries Column</label>
                    </td>
                    <td align="left">
                        <input type="text" id="countries_col" name="countries_col" maxlength="3" size="3">
                    </td>
                </tr>
                <tr>
                    <td colspan="3" align="center">
                        <table id="criteria_table">
                            <tr>
                                <td align="left">
                                    <br/>
                                    <b>Criteria to Import</b>
                                </td>
                                <td>
                                    <button id="add_criteria" name="add_criteria" type="button" onClick="addCriteriaFields('''+category_array+''')">Add New Criteria</button>
                                </td>
                            </tr>
                            <tr>
                                <td align="right">
                                    <label for="criteria_1">Criteria 1</label>
                                </td>
                                <td align="left">
                                    <input type="text" id="criteria_1" name="criteria_1">
                                </td>
                                <td align="right">
                                    <label for="category_1">Category 1</label>
                                </td>
                                <td align="left">
                                    <select id="category_1" name="category_1">'''
                                    
    for category in neo4j.get_category_list():
        data = data+'<option value="'+str(category)+'">'+str(category)+'</option>'
    
    data = data+'''                 </select>
                                </td>
                                <td align="right">
                                    <label for="col_num1">Column</label>
                                </td>
                                <td align="left">
                                    <input type="text" id="col_num1" name="col_num1" maxlength="3" size="3">
                                </td>
                                <td>
                                    <button id="remove_criteria1" name="remove_criteria1" type="button" onClick="removeCriteriaFields(this.id)">Remove Criteria</button>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <input type="hidden" id="criteria_count" name="criteria_count" value="1">
                <tr>
                    <td align="center" colspan="2">
                        <label id="error_panel" name="error_panel" />
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align:center">
                        <input type="submit" value="Import Data">
                    </td>
                </tr>
            </table>
        </form>
    </div>
</body>
</html>'''

    return data
    