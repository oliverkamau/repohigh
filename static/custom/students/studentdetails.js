
$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
formatDate();
feeChange();
studentImage("");
searchDorm();
dormChange();
searchCampus();
campusChange();
searchNationality();
countryChange();
countyChange();
subCountyChange();
locationChange();
subLocationChange();
villageChange();
searchDenomination();
denominationChange();
searchSources();
sourcesChange();
searchYear();
yearChange();
searchHealth();
searchStatus();
statusChange();
healthChange();
searchDocument();
searchClass();
classChange();
searchParent();
parentChange();
searchFeeCategory();
documentChange();
saveStudent()
getStudents()
editStudent()
newStudent()
deleteStudent()
saveDocs()
viewDocs()
deleteDocs()
})
function newStudent() {
   $('#newStudent').click(function () {
       clearPage();
   })
}
function saveDocs(){
   $('#saveDocs').click(function () {

        if($('#studentCode').val()==='' || $('#studentDocument').val()==='' || $( '#importDocs' )[0].files.length===0){
            bootbox.alert('Student or File not selected');
        }
        else {
            var formData = new FormData();
            formData.append( 'document_file', $( '#importDocs' )[0].files[0]);
            formData.append('stud_doc_document',$('#studentDocument').val());
            formData.append('stud_doc_student',$('#studentCode').val());
            $.ajax({
                type: 'POST',
                url: 'uploadstudentdocs',
                data: formData,
                processData: false,
                contentType: false
            }).done(function (s) {
               swal({
         type: 'success',
         title: 'Success',
         text: s.success,
         showConfirmButton: true
     })

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })

        }
   })
}
function viewDocs(){
   $('#viewDocs').click(function () {

        if($('#studentCode').val()==='' || $('#studentDocument').val()===''){
            bootbox.alert('Student or File not selected');
        }
        else {
            var formData = new FormData();
            formData.append('stud_doc_document',$('#studentDocument').val());
            formData.append('stud_doc_student',$('#studentCode').val());
            $.ajax({
                type: 'POST',
                url: 'viewstudentdocs',
                data: formData,
                processData: false,
                contentType: false
            }).done(function (s) {
               if (s.length === 0 ) {
               bootbox.alert('No File Found')
               }
               else{
               window.open(s.url);
               }

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })

        }
   })
}
function deleteDocs() {
   $('#deleteDocs').click(function () {

        if($('#studentCode').val()==='' || $('#studentDocument').val()===''){
            bootbox.alert('Student or File not selected');
        }
        else {
            var formData = new FormData();
            formData.append('stud_doc_document',$('#studentDocument').val());
            formData.append('stud_doc_student',$('#studentCode').val());
            $.ajax({
                type: 'POST',
                url: 'deletestudentdocs',
                data: formData,
                processData: false,
                contentType: false
            }).done(function (s) {
               bootbox.alert(s.success)


            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })

        }
   })
}
function deleteStudent() {
     $('#studTable').on('click','.btn-deletestudent',function (s) {
        var data = $(this).closest('tr').find('#delete-student').val();
        bootbox.confirm("Are you sure want to delete this Student?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deletestudent/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          bootbox.hideAll()
          getStudents()
          bootbox.alert(s.success)


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function saveStudent(){
    $('#saveStudent').click(function () {

        if($('#upi').val()==''){
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'UPI Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
        else if($('#admNo').val()==='') {
            swal({
                title: 'Alert!',
                type: 'info',
                text: 'AdmNo Field is Mandatory',
                confirmButtonText: 'OK'
            })
        }
            else if($('#studentName').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Name Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#gender').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Gender Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#studentClass').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Class Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#feeCategory').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Fee Category Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#dorm').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Dorm Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#parent').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Parent Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#studentCounty').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'County Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#subCounty').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Sub County Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#dob').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Date of Birth Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#birthCertNo').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Birth Cert Number Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
        else {
            var main = $('#main-form').serializeArray();
            var contact = $('#contact-form').serializeArray();
            var details = $('#other-form').serializeArray();
            var formData = new FormData();
            for (var i = 0; i < main.length; i++) {
                formData.append(main[i].name, main[i].value);
            }
            for (var j = 0; j < contact.length; j++) {
                formData.append(contact[j].name, contact[j].value);
            }
            for (var k = 0; k < details.length; k++) {
                formData.append(details[k].name, details[k].value);
            }
            formData.append('student_photo', $('#student-avatar')[0].files[0]);

            var url = '';
            if ($('#studentCode').val() === '') {
                url = 'addstudent'
            } else {
                url = 'updatestudent/' + $('#studentCode').val()
                formData.append('adm_no', $('#admNoEdit').val());
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: formData,
                processData: false,
                contentType: false
            }).done(function (s) {
                clearPage()
                getStudents()
                swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })
            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
            })

        }
	})
}
function getStudents() {
     $.ajax({
        type: 'GET',
        url: 'getstudents',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#studTable').DataTable().destroy();
        $("#studTable tbody").empty();
        $.each(s,function(i,item){
            $("#studTable tbody").append(
                "<tr>"
                +"<td>"+item.admNo+"</td>"
                +"<td>"+item.name+"</td>"
                +"<td>"+item.birthDate+"</td>"
                +"<td>"+item.admDate+"</td>"
                +"<td>"+item.completionDate+"</td>"
                +"<td>"+item.dorm+"</td>"
                +"<td>"+item.studentClass+"</td>"
                +"<td>"+item.email+"</td>"
                +"<td>"+item.phone+"</td>"
                +"<td>"+item.parent+"</td>"
                +"<td>"+item.gender+"</td>"
                +"<td>"+item.nationality+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.studentCode+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-student" name="id" value='+item.studentCode+'></form><button class="btn btn-outline-danger btn-sm btn-deletestudent" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
        })
        $('#studTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function studentImage(url){
        $("#student-avatar").fileinput('destroy').fileinput({
            overwriteInitial: true,
            maxFileSize: 1500,
            showClose: false,
            showCaption: false,
            browseLabel: '',
            removeLabel: '',
            browseIcon: '<i class="fa fa-folder-open"></i>',
            removeIcon: '<i class="fa fa-times"></i>',
            removeTitle: 'Cancel or reset changes',
            elErrorContainer: '#kv-avatar-errors',
            msgErrorClass: 'alert alert-block alert-danger',
            defaultPreviewContent: '<img src="' + url + '"  style="height:13em;width:230px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#dob').val([year, month, day].join('-'))
    $('#completionDate').val([year, month, day].join('-'))
    $('#admDate').val([year, month, day].join('-'))

}

function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class Admitted',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchclasses',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function editStudent(){
    $('#studTable').on('click','.btn-editstudent',function (s) {
        var data=$(this).closest('tr').find('#edit-student').val();
        $.ajax({
            type: 'GET',
            url: 'editstudent/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#studentCode').val(s[0].studentCode);
            $('#studentName').val(s[0].name);
            $('#admNo').val(s[0].admNo);
            $('#admNoEdit').val(s[0].admNo);
            $('#admNo').prop('disabled',true)
            $('#upi').val(s[0].upi);
            $('#gender').val(s[0].gender);
            $('#term').val(s[0].term);
            $('#address').val(s[0].address);
            $('#studentEmail').val(s[0].email);
            $('#parentPhone').val(s[0].parentPhone);
             $('#studentPhone').val(s[0].phone);
            $('#admDate').val(s[0].admDate);
            $('#dob').val(s[0].birthDate);
            $('#completionDate').val(s[0].completionDate);
            $('#birthCertNo').val(s[0].birthCertNo);
            $('#marks').val(s[0].marks);
            $('#grade').val(s[0].grade);
            $('#primarySchool').val(s[0].primarySchool);
            $('#indexNo').val(s[0].indexNo)

            if (s[0].categoryCode) {
                var $newCat = $("<option selected='selected' value='" + s[0].categoryCode + "'>'+s[0].categoryName+'</option>").val(s[0].categoryCode.toString()).text(s[0].categoryName)

                $('#fee_frm').append($newCat).trigger('change');
                $('#feeCategory').val(s[0].categoryCode)
            }
            else {
                $('#fee_frm').empty();
                $('#feeCategory').val('')

            }

			if (s[0].dormCode) {
			    var $newDorm= $("<option selected='selected' value='" + s[0].dormCode + "'>'+s[0].dormName+'</option>").val(s[0].dormCode.toString()).text(s[0].dormName)

               $('#dorm_frm').append($newDorm).trigger('change');
			    $('#dorm').val(s[0].dormCode)
			    }
			    else {
			    $('#dorm_frm').empty();
			    $('#dorm').val('')

			}
			if (s[0].campusCode) {
			    var $newCam = $("<option selected='selected' value='" + s[0].campusCode + "'>'+s[0].campusName+'</option>").val(s[0].campusCode.toString()).text(s[0].campusName)

               $('#campus_frm').append($newCam).trigger('change');
			    $('#campus').val(s[0].campusCode)
			    }
			    else {
			    $('#campus_frm').empty();
			    $('#campus').val('')

			}
			if (s[0].classCode) {
			    var $newCl = $("<option selected='selected' value='" + s[0].classCode + "'>'+s[0].className+'</option>").val(s[0].classCode.toString()).text(s[0].className)

               $('#class_frm').append($newCl).trigger('change');
			    $('#studentClass').val(s[0].classCode)
			    }
			    else {
			    $('#class_frm').empty();
			    $('#studentClass').val('')

			}
			if (s[0].parentCode) {
			    var $newParent = $("<option selected='selected' value='" + s[0].parentCode + "'>'+s[0].parentName+'</option>").val(s[0].parentCode.toString()).text(s[0].parentName)

               $('#parent_frm').append($newParent).trigger('change');
			    $('#parent').val(s[0].parentCode)
			    }
			    else {
			    $('#parent_frm').empty();
			    $('#parent').val('')

			}
			if (s[0].countryCode) {
			    var $newCountry = $("<option selected='selected' value='" + s[0].countryCode + "'>'+s[0].countryName+'</option>").val(s[0].countryCode.toString()).text(s[0].countryName)

               $('#nationality_frm').append($newCountry).trigger('change');
			    $('#nationality').val(s[0].countryCode)
                searchCounties(s[0].countryCode)
			    }
			    else {
			    $('#nationality_frm').empty();
			    $('#nationality').val('')

			}
			if (s[0].countyCode) {
			    var $newCounty = $("<option selected='selected' value='" + s[0].countyCode + "'>'+s[0].countyName+'</option>").val(s[0].countyCode.toString()).text(s[0].countyName)
               $('#county_frm').append($newCounty).trigger('change');
			   $('#studentCounty').val(s[0].countyCode)
                searchSubCounty(s[0].countyCode)

			    }
			    else {
			    $('#county_frm').empty();
			    $('#studentCounty').val('')

			}
			if (s[0].subCountyCode) {
			    var $newSubCounty = $("<option selected='selected' value='" + s[0].subCountyCode + "'>'+s[0].subCountyName+'</option>").val(s[0].subCountyCode.toString()).text(s[0].subCountyName)

               $('#subcounty_frm').append($newSubCounty).trigger('change');
			    $('#subCounty').val(s[0].subCountyCode)
                searchLocation(s[0].countyCode)
			    }
			    else {
			    $('#subcounty_frm').empty();
			    $('#subCounty').val('')

			}
			if (s[0].locationCode) {
			    var $newLocation = $("<option selected='selected' value='" + s[0].locationCode + "'>'+s[0].locationName+'</option>").val(s[0].locationCode.toString()).text(s[0].locationName)

               $('#location_frm').append($newLocation).trigger('change');
			    $('#location').val(s[0].locationCode)
                searchSubLocation(s[0].locationCode)
			    }
			    else {
			    $('#location_frm').empty();
			    $('#location').val('')

			}
			if (s[0].subLocationCode) {
			    var $newSubLocation = $("<option selected='selected' value='" + s[0].subLocationCode + "'>'+s[0].subLocationName+'</option>").val(s[0].subLocationCode.toString()).text(s[0].subLocationName)

               $('#sublocation_frm').append($newSubLocation).trigger('change');
			    $('#subLocation').val(s[0].subLocationCode)
                searchVillage(s[0].subLocationCode)
			    }
			    else {
			    $('#sublocation_frm').empty();
			    $('#subLocation').val('')

			}
			if (s[0].villageCode) {
			    var $newVillage = $("<option selected='selected' value='" + s[0].villageCode + "'>'+s[0].villageName+'</option>").val(s[0].villageCode.toString()).text(s[0].villageName)

               $('#village_frm').append($newVillage).trigger('change');
			    $('#village').val(s[0].villageCode)
			    }
			    else {
			    $('#village_frm').empty();
			    $('#village').val('')

			}
			if (s[0].denominationCode) {
			    var $newDen = $("<option selected='selected' value='" + s[0].denominationCode + "'>'+s[0].denominationName+'</option>").val(s[0].denominationCode.toString()).text(s[0].denominationName)

               $('#denomination_frm').append($newDen).trigger('change');
			    $('#religion').val(s[0].denominationCode)
			    }
			    else {
			    $('#denomination_frm').empty();
			    $('#religion').val('')

			}
			if (s[0].healthCode) {
			    var $newHealth = $("<option selected='selected' value='" + s[0].healthCode + "'>'+s[0].healthName+'</option>").val(s[0].healthCode.toString()).text(s[0].healthName)

               $('#healthstatus_frm').append($newHealth).trigger('change');
			    $('#healthStatus').val(s[0].healthCode)
			    }
			    else {
			    $('#healthstatus_frm').empty();
			    $('#healthStatus').val('')

			}

			if (s[0].sourceCode) {
			    var $newSource = $("<option selected='selected' value='" + s[0].sourceCode + "'>'+s[0].sourceName+'</option>").val(s[0].sourceCode.toString()).text(s[0].sourceName)

               $('#sources_frm').append($newSource).trigger('change');
			   $('#sources').val(s[0].sourceCode)

			    } else {
			    $('#sources_frm').empty();
			    $('#sources').val('')

			}
			if (s[0].statusCode) {
			    var $newStat = $("<option selected='selected' value='" + s[0].statusCode + "'>'+s[0].statusName+'</option>").val(s[0].statusCode.toString()).text(s[0].statusName)

               $('#studentstatus_frm').append($newStat).trigger('change');
			   $('#studentStatus').val(s[0].statusCode)

			    } else {
			    $('#studentstatus_frm').empty();
			    $('#studentStatus').val('')

			}
			if (s[0].yearCode) {
			    var $newYear = $("<option selected='selected' value='" + s[0].yearCode + "'>'+s[0].yearName+'</option>").val(s[0].yearCode.toString()).text(s[0].yearName)

               $('#year_frm').append($newYear).trigger('change');
			   $('#year').val(s[0].yearCode)

			    } else {
			    $('#year_frm').empty();
			    $('#year').val('')

			}
			if(s[0].url) {
                studentImage(s[0].url)
            }
            else{
			    studentImage("")
            }

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function clearPage(){
    $('#studentCode').val('');
    $('#admNoEdit').val('');
    $('#admNo').prop('disabled',false);
    $('#main-form')[0].reset()
    $('#contact-form')[0].reset()
    $('#other-form')[0].reset()
    $('#fee_frm').empty();
    $('#feeCategory').val('')
    $('#dorm_frm').empty();
	$('#dorm').val('')
    $('#campus_frm').empty();
	$('#campus').val('')
    $('#class_frm').empty();
	$('#studentClass').val('')
    $('#parent_frm').empty();
	$('#parent').val('')
    $('#nationality_frm').empty();
	$('#nationality').val('')
    $('#county_frm').empty();
	$('#studentCounty').val('')
    $('#subcounty_frm').empty();
	$('#subCounty').val('')
    $('#location_frm').empty();
	$('#location').val('')
    $('#sublocation_frm').empty();
	$('#subLocation').val('')
    $('#village_frm').empty();
	$('#village').val('')
    $('#denomination_frm').empty();
	$('#religion').val('')
    $('#healthstatus_frm').empty();
	$('#healthStatus').val('')
    $('#sources_frm').empty();
    $('#sources').val('')
    $('#studentstatus_frm').empty();
    $('#studentStatus').val('')
    $('#year_frm').empty();
    $('#year').val('')
    $('#document_frm').empty()
    $('#studentDocument').val('')
    formatDate()
    studentImage("")
}
function searchParent() {

     $('#parent_frm').select2({
           placeholder: 'Names',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchparent',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function searchDocument() {
     $('#document_frm').select2({
           placeholder: 'Document',
           allowClear: true,
           width: '50%',
           ajax: {
             delay: 250,
             url: 'searchdocs',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}

function searchFeeCategory() {
     $('#fee_frm').select2({
           placeholder: 'Fees',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchfeecategory',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}

function searchDorm() {
        $('#dorm_frm').select2({
            placeholder: 'House',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchdorms',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchCampus() {
     $('#campus_frm').select2({
           placeholder: 'Campus',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchcampus',
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function countryChange() {
    $('#nationality_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#nationality').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchCounties(data.id)

    });
    $("#nationality_frm").on("select2:unselecting", function(e) {
    $('#nationality').val('')
 });
}
function documentChange() {
    $('#document_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentDocument').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#document_frm").on("select2:unselecting", function(e) {
    $('#studentDocument').val('')
 });
}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentClass').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#studentClass').val('')
 });
}
function campusChange() {
    $('#campus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#campus').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#campus_frm").on("select2:unselecting", function(e) {
    $('#campus').val('')
 });
}
function feeChange() {
    $('#fee_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#feeCategory').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#fee_frm").on("select2:unselecting", function(e) {
    $('#feeCategory').val('')
 });
}
function parentChange() {
    $('#parent_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#parent').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#parent_frm").on("select2:unselecting", function(e) {
    $('#parent').val('')
 });
}
function dormChange() {
    $('#dorm_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#dorm').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#dorm_frm").on("select2:unselecting", function(e) {
    $('#dorm').val('')
 });
}
function countyChange() {
    $('#county_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentCounty').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchSubCounty(data.id)

    });
    $("#county_frm").on("select2:unselecting", function(e) {
    $('#studentCounty').val('')
 });
}
function subLocationChange() {
   $('#sublocation_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subLocation').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchVillage(data.id)

    });
    $("#sublocation_frm").on("select2:unselecting", function(e) {
    $('#subLocation').val('')
 });
}
function villageChange() {
   $('#village_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#village').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#village_frm").on("select2:unselecting", function(e) {
    $('#village').val('')
 });
}
function denominationChange() {
   $('#denomination_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#religion').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#denomination_frm").on("select2:unselecting", function(e) {
    $('#religion').val('')
 });
}
function sourcesChange() {
   $('#sources_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#sources').val(data.id)

        // console.log('country is: '+$('#country-id').val())

    });
    $("#sources_frm").on("select2:unselecting", function(e) {
    $('#sources').val('')
 });
}
function subCountyChange() {
    $('#subcounty_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subCounty').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchLocation(data.id)

    });
    $("#subcounty_frm").on("select2:unselecting", function(e) {
    $('#subCounty').val('')
 });
}
function locationChange() {
    $('#location_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#location').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchSubLocation(data.id)

    });
    $("#location_frm").on("select2:unselecting", function(e) {
    $('#location').val('')
 });
}
function yearChange() {
    $('#year_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#year').val(data.id)
    });
    $("#year_frm").on("select2:unselecting", function(e) {
    $('#year').val('')
 });
}
function healthChange() {
    $('#healthstatus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#healthStatus').val(data.id)
    });
    $("#healthstatus_frm").on("select2:unselecting", function(e) {
    $('#healthStatus').val('')
 });
}
function statusChange() {
    $('#studentstatus_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentStatus').val(data.id)
    });
    $("#studentstatus_frm").on("select2:unselecting", function(e) {
    $('#studentStatus').val('')
 });
}
function searchNationality() {
        $('#nationality_frm').select2({
            placeholder: 'Countries',
            allowClear: true,
            width: '50%',
            ajax: {
                delay: 250,
                url: 'searchcountry',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchDenomination() {
        $('#denomination_frm').select2({
            placeholder: 'Denomination',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchdenominations',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchSources() {
        $('#sources_frm').select2({
            placeholder: 'Sources',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchstudentsources',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchYear() {
        $('#year_frm').select2({
            placeholder: 'Year',
            allowClear: true,
            width: '16%' ,
            ajax: {
                delay: 250,
                url: 'searchyears',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchHealth() {
        $('#healthstatus_frm').select2({
            placeholder: 'Conditions',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchhealthstatus',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchStatus() {
        $('#studentstatus_frm').select2({
            placeholder: 'Status',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchstudentstatus',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchSubCounty(id) {
        $('#subcounty_frm').select2({
            placeholder: 'SubCounty',
            allowClear: true,
            width: '50%' ,
            ajax: {
                delay: 250,
                url: 'searchsubcounty/'+id,
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function searchCounties(id) {

     $('#county_frm').select2({
           placeholder: 'Counties',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchcounties/'+id,
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function searchLocation(id) {

     $('#location_frm').select2({
           placeholder: 'Location',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchlocation/'+id,
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function searchSubLocation(id) {

     $('#sublocation_frm').select2({
           placeholder: 'SubLocation',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchsublocation/'+id,
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}
function searchVillage(id) {

     $('#village_frm').select2({
           placeholder: 'Village',
           allowClear: true,
           width: '50%' ,
           ajax: {
             delay: 250,
             url: 'searchvillage/'+id,
             data: function (params) {
                 console.log("AA", params);
                 return {
                     query: params.term,
                     gotoPage: params.page
                 }
             },

             processResults: function (data,params) {
                 params.page = params.page || 1;
                 console.log('data: ', data);
                 return {
                   results: data.results
                 };
             }

         }
     })
}