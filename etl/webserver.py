import cgi
import traceback

# Do not change this name function... It needs to be webserver:app so
# gunicorn (python webserver) finds it
def app(environ, start_response):
    try:
        param = cgi.parse_qs(environ['QUERY_STRING']).get('param', [''])[0]
        data = """<html>
                    <script>
                        function setDelimiterVisibility() {
                            var e = document.getElementById("source_file_type");
                            var fileType = e.options[e.selectedIndex].value;
                            if (fileType == "csv")
                                document.getElementById("delimiter_char_tr").style.visibility = 'visible';
                            else
                                document.getElementById("delimiter_char_tr").style.visibility = 'hidden';
                        }
                        
                        function setCountriesColVisibility() {
                            var e = document.getElementById("country_name");
                            var selectedCoutnry = e.options[e.selectedIndex].value;
                            if (selectedCoutnry == "multiple")
                                document.getElementById("countries_col_tr").style.visibility = 'visible';
                            else
                                document.getElementById("countries_col_tr").style.visibility = 'hidden';
                        }
                        
                        
                        function addCriteriaFields() {
                            var criteriaCount = document.getElementById("criteria_count").value;
                            criteriaCount = parseInt(criteriaCount, 10) + 1;
                            document.getElementById("criteria_count").value = criteriaCount;

                            var table = document.getElementById("criteria_table");
                            var rowCount = table.rows.length;
                            var row = table.insertRow(rowCount);
                            
                            var cell1 = row.insertCell(0);
                            cell1.align = "right";
                            var element1 = document.createElement("label");
                            element1.for = "criteria_" + criteriaCount;
                            element1.innerHTML="Criteria " + criteriaCount;
                            cell1.appendChild(element1);
                            
                            var cell2 = row.insertCell(1);
                            var element2 = document.createElement("select");
                            element2.id = "criteria_" + criteriaCount;
                            element2.name = "criteria_" + criteriaCount;
                            var option = document.createElement("option");
                            option.text = "Paid Annual Leave";
                            option.value = "paid_annual_leave";
                            element2.add(option);
                            var option2 = document.createElement("option");
                            option2.text = "Minimum Wage";
                            option2.value = "minimum_wage";
                            element2.add(option2);
                            var option3 = document.createElement("option");
                            option3.text = "Unemployment Rate";
                            option3.value = "unemplyment_rate";
                            element2.add(option3);
                            cell2.appendChild(element2);
                            
                            var cell3 = row.insertCell(2);
                            var element3 = document.createElement("label");
                            element3.for = "col_num" + criteriaCount;
                            element3.innerHTML="Column ";
                            cell3.appendChild(element3);
                            
                            var cell4 = row.insertCell(3);
                            var element4 = document.createElement("input");
                            element4.type = "text";
                            element4.id = "col_num" + criteriaCount;
                            element4.name = "col_num" + criteriaCount;
                            element4.maxlength = "3";
                            element4.size = "3";
                            cell4.appendChild(element4);
                            
                            var cell5 = row.insertCell(4);
                            var element5 = document.createElement("button");
                            element5.type = "button";
                            element5.id = "remove_criteria" + criteriaCount;
                            element5.name = "remove_criteria" + criteriaCount;
                            element5.innerHTML = "Remove Criteria";
                            element5.onclick = function() { removeCriteriaFields(this.id); }
                            cell5.appendChild(element5);
                            
                            /*var cell6 = row.insertCell(5);
                            var element6 = document.createElement("button");
                            element6.type = "button";
                            element6.id = "add_criteria" + criteriaCount;
                            element6.name = "add_criteria" + criteriaCount;
                            element6.innerHTML = "Add New Criteria";
                            element6.onclick = addCriteriaFields;
                            cell6.appendChild(element6);*/
                        }
                        
                        function removeCriteriaFields(id) {
                            var e = document.getElementById(id).parentNode.parentNode;
                            e.parentNode.removeChild(e);

                            var criteriaCount = document.getElementById("criteria_count").value;
                            criteriaCount = parseInt(criteriaCount, 10) - 1;
                            document.getElementById("criteria_count").value = criteriaCount;
                            
                            return false;
                        }
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
                            <form id="etlconfig" name="etlconfig" method="post" action="./runEtlConfig.py">
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
                                            <select id ="source_file_type" name="source_file_type" onchange="setDelimiterVisibility()">
                                                <option value="csv" selected="true">CSV</option>
                                                <option value="excel">Excel</option>
                                                <option value="html">Tabular HTML</option>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr id="delimiter_char_tr">
                                        <td align="right">
                                            <label for="delimiter_char">Delimiter Character</label>
                                        </td>
                                        <td align="left">
                                            <input type="text" id="delimiter_char" name="delimiter_char" maxlength="1" size="3">
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="right">
                                            <label for="country_name">Country</label>
                                        </td>
                                        <td align="left">
                                            <select id ="country_name" name="country_name" onchange="setCountriesColVisibility()">
                                                <option value="multiple" selected="true">MULTIPLE</option>
                                                <option value="Australia">Australia</option>
                                                <option value="Canada">Canada</option>
                                                <option value="France">France</option>
                                                <option value="Germany">Germany</option>
                                                <option value="South Africa">South Africa</option>
                                                <option value="UAE">UAE</option>
                                                <option value="UK">UK</option>
                                                <option value="USA">USA</option>
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
                                                        <button id="add_criteria" name="add_criteria" type="button" onClick="addCriteriaFields()">Add New Criteria</button>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="right">
                                                        <label for="criteria_1">Criteria 1</label>
                                                    </td>
                                                    <td align="left">
                                                        <select id="criteria_1" name="criteria_1">
                                                            <option value="paid_annual_leave" selected="true">Paid Annual Leave</option>
                                                            <option value="minimum_wage">Minimum Wage</option>
                                                            <option value="unemplyment_rate">Unemployment Rate</option>
                                                        </select>
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
                </html>"""
                
        # This is how we play with the HTTP
        status = '200 OK'
        response_headers = [
            ('Content-type','text/html'),
            ('Content-Length', str(len(data)))
        ]
        start_response(status, response_headers)
        
        # This is how we return the HTML code
        return iter([data])
    except Exception, e:
        data = traceback.format_exc()
        status = '200 OK'
        response_headers = [
            ('Content-type','text/plain'),
            ('Content-Length', str(len(data)))
        ]
        start_response(status, response_headers)
        
        # This is how we return the HTML code
        return iter([data])
