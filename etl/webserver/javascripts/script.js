function submitFormInPopUp() 
{
    document.getElementById("potential_csv_submit").value = 'true'
    window.open('','potential_csv_popup','location=no, status=no, toolbar=no, scrollbars=yes, width=730, height=500');

    document.etlconfig.target = "potential_csv_popup"
    document.etlconfig.submit(); 
}

function setSourceFileType() {
    var e = document.getElementById("source_file_type");
    var fileType = e.options[e.selectedIndex].value;
    
    if (fileType == "csv")
        document.getElementById("delimiter_char_tr").style.visibility = 'visible';
    else
        document.getElementById("delimiter_char_tr").style.visibility = 'hidden';
        
    if (fileType == "html") {
        document.getElementById("potential_csv_tr").style.visibility = 'visible';
        document.getElementById("has_headers_tr").style.visibility = 'visible';
    }
    else {
        document.getElementById("potential_csv_tr").style.visibility = 'hidden';
        document.getElementById("has_headers_tr").style.visibility = 'hidden';
    }
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
    var element2 = document.createElement("input");
    element2.type = "text"
    element2.id = "criteria_" + criteriaCount;
    element2.name = "criteria_" + criteriaCount;
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
}

function removeCriteriaFields(id) {
    var criteriaCount = parseInt( document.getElementById("criteria_count").value, 10) - 1;
    if (criteriaCount > 0) {
        var e = document.getElementById(id).parentNode.parentNode;
        e.parentNode.removeChild(e);
    
        document.getElementById("criteria_count").value = criteriaCount;
    }
    
    return false;
}