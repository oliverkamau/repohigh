$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
studentImage("");
formatDate();
searchClass();
classChange();
studentChange();
getStudents();
changeStatus();
getDynamicUrl();
searchClassMvClass()
searchNextMvClass()
nextChange();
moveChange();
processTrans();
unmovedStudents();
movedStudents();
assignallStudents();
unassignallStudent();
assignStudents();
unassignStudents();
searchTable();
editStudent();
searchTableClass();
tableSearchChange();
$('#studentmovement').show();
$('#classmovement').hide();
$('#resume').hide()
$('#noResume').show()

})
function getDynamicUrl() {
   $.ajax({
          type: 'GET',
          url: 'dynamicaddress',
      }).done(function (s) {
          spinner=s.url
      }).fail(function (xhr, error) {
          bootbox.alert(xhr.responseText)

      });
}

function assignStudents() {
 $('#assignSelected').on('click',function (s) {
  if(assigned.length===0 || $('#classmvClassCode').val()==='' || $('#nextMvClassCode').val()==='' || $('#classMvterm').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students,classes or term selected to move',
         confirmButtonText: 'OK'
      })
  } else {
         swal({
              title: "Moving...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
      var data = new FormData();
      data.append("classcode", $('#classmvClassCode').val());
      data.append("reason", $('#classMvReason').val());
      data.append("nextclasscode", $('#nextMvClassCode').val());
      data.append("movementdate", $('#classMvDate').val());
      data.append('students', JSON.stringify(assigned));
      data.append('term',$('#classMvterm').val());
      $.ajax({
          type: 'POST',
          url: 'assignstudents',
          data: data,
          processData: false,
          contentType: false,
      }).done(function (s) {
            swal.close()
          getLoaded()
          getUnloaded()
          assigned=[]
        // swal({
        //  type: 'success',
        //  title: 'Success',
        //  text: s.success,
        //  showConfirmButton: true,
     //})
      }).fail(function (xhr, error) {
            swal.close()
          bootbox.alert(xhr.responseText)

      });
  }
    });

}
function unassignStudents() {
 $('#unAssignSelected').on('click',function (s) {
  if(unassigned.length===0 || $('#classmvClassCode').val()==='' || $('#nextMvClassCode').val()==='' || $('#classMvterm').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students,class or term selected to move',
         confirmButtonText: 'OK'
      })
  } else {
              swal({
              title: "Moving...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
           var data = new FormData();
          data.append("classcode", $('#classmvClassCode').val());
          data.append("reason", $('#classMvReason').val());
          data.append("nextclasscode", $('#nextMvClassCode').val());
          data.append("movementdate", $('#classMvDate').val());
          data.append('students', JSON.stringify(unassigned));
           $.ajax({
               type: 'POST',
               url: 'unassignstudents',
               data: data,
               processData: false,
               contentType: false,
           }).done(function (s) {
            swal.close()
            getUnloaded()
            getLoaded()
            unassigned=[]

      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)
      });
       }
    });
}
function assignallStudents() {
$('#assignAll').on('click',function (s) {
      if($('#classmvClassCode').val()==='' || $('#nextMvClassCode').val()==='' || $('#classMvterm').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No classes or term selected to make transfers',
         confirmButtonText: 'OK'
      })
  } else {
          swal({
              title: "Moving...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
          var data = new FormData();
            data.append("classcode", $('#classmvClassCode').val());
            data.append("reason", $('#classMvReason').val());
            data.append("nextclasscode", $('#nextMvClassCode').val());
            data.append("movementdate", $('#classMvDate').val());
          $.ajax({
              type: 'POST',
              url: 'assignallstudents',
              data: data,
              processData: false,
              contentType: false,
          }).done(function (s) {
            swal.close()
              getLoaded()
              getUnloaded()
      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)

      });
      }
    });
}
function unassignallStudent() {
$('#unAssignAll').on('click',function (s) {
     if($('#classmvClassCode').val()==='' || $('#nextMvClassCode').val()===''||$('#classMvterm').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No classes or term selected to make transfers',
         confirmButtonText: 'OK'
      })
  } else {
            swal({
              title: "Moving...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
         var data = new FormData();
           data.append("classcode", $('#classmvClassCode').val());
           data.append("reason", $('#classMvReason').val());
           data.append("nextclasscode", $('#nextMvClassCode').val());
           data.append("movementdate", $('#classMvDate').val());
         $.ajax({
             type: 'POST',
             url: 'unassignallstudents',
             data: data,
             processData: false,
             contentType: false,
         }).done(function (s) {
             swal.close()
             getLoaded()
             getUnloaded()
      }).fail(function (xhr, error) {
          swal.close()
            bootbox.alert(xhr.responseText)


      });
     }
    });
}

function changeStatus(){
$('#action').change(function () {
    var classCode = $('#classCode').val();
    var action = $('#action').val();
    var term = $('#term').val();
    var date = $('#date').val();
    var reason = $('#reason').val();

        if(action==='S' || action==='ES' || action ==='EX' || action==='T'){
          var student = $('#studentCode').val();

             $('#studentmovement').show();
             $('#classmovement').hide();
             if(action==='S'||action==='ES'){
                 $('#resume').show()
                 $('#noResume').hide()
             }
             else{
                 $('#resume').hide()
                 $('#noResume').show()
             }
         }


        else if(action === 'CM'){
         $('#studentmovement').hide();
         $('#classmovement').show();


        }
})
}
function searchTable(){
$('#statii').change(function () {
    var action = $('#statii').val();


        if(action===''){
           getStudents();
        }else {

         $.ajax({
        type: 'GET',
        url: 'getspecificstudents/'+action,
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
                +"<td>"+item.status+"</td>"
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

})
}

function searchReload(id){

         $.ajax({
        type: 'GET',
        url: 'getspecificstudents/'+id,
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
                +"<td>"+item.status+"</td>"
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

function getStudentsClass(id) {
     $.ajax({
        type: 'GET',
        url: 'searchbyclass/'+id,
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
                +"<td>"+item.status+"</td>"
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
function unmovedStudents() {
$('#unAssignedTbl').on('change','.stud-check',function (s) {

    var data=$(this).closest('tr').find('#studCode').val();

    if(this.checked){
    if(assigned.indexOf(data) === -1){

        assigned.push(data)
        console.log(assigned)
    } else{
        console.log('Element '+data+' exists')

    }
    }
    else{
        assigned = jQuery.grep(assigned, function(value) {
  return value !== data;
});
    }
    });

}
function movedStudents() {
$('#assignedTbl').on('change','.stud-check',function (s) {

    var data=$(this).closest('tr').find('#studCode').val();

    if(this.checked){
    if(unassigned.indexOf(data) === -1){
        unassigned.push(data)
        console.log(unassigned)
    } else{
        console.log('Element '+data+' exists')
    }
    }
    else{
       unassigned = jQuery.grep(unassigned, function(value) {
  return value !== data;
});
    }
    });

}
function clearpage(){
    $('#classCode').val('');
    $('#studentCode').val('');
    $('#action').val('');
    $('#term').val('');
    $('#reason').val('');
    $('#term').val('');
    $('#class_frm').empty();
    $('#student_frm').empty();
    formatDate()
    studentImage("")
}
function processTrans(){
 $('#process').click(function () {
     var classCode = $('#classCode').val();
    var action = $('#action').val();
    var term = $('#term').val();
    var date = $('#date').val();
    var reason = $('#reason').val();
    var resume = $('#resumeDate').val();

        if(action==='S' || action==='ES' || action ==='EX' || action==='T'){
          var student = $('#studentCode').val();
         if(student === ''||classCode === '' || term === '' || date === '' ){
        swal({
          title: 'Alert!',
          type: 'info',
          text: 'Fields Student,Class,Term and Date is Mandatory',
         confirmButtonText: 'OK'
      })
     }else {
             var formData = new FormData();
             formData.append('movement_class', classCode);
             formData.append('movement_student', student);
             formData.append('movement_action', action);
             formData.append('movement_term', term);
             formData.append('movement_date', date);
             formData.append('movement_reason', reason);
             formData.append('resume_date',resume);
                    $.ajax({
                        type: 'POST',
                        url: 'studentmovement',
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
                        if($('#statii').val()!=='') {
                            searchReload($('#statii').val())
                        }else{
                            getStudents();
                        }
             clearpage()
             }).fail(function (xhr, error) {
                 bootbox.alert(xhr.responseText)
             })
         }

        }
     //    else if(action === 'CM'){
     //      var data = new FormData();
     //        data.append('movement_class',classCode);
     //        data.append('movement_action',action);
     //        data.append('movement_term',term);
     //        data.append('movement_date',date);
     //        data.append('movement_reason',reason);
     //
     //        $.ajax({
     //            type: 'POST',
     //            url: 'classmovements',
     //            data: formData,
     //            processData: false,
     //            contentType: false
     //        }).done(function (s) {
     //           swal({
     //     type: 'success',
     //     title: 'Success',
     //     text: s.success,
     //     showConfirmButton: true
     // })
     //
     //        }).fail(function (xhr, error) {
     //            bootbox.alert(xhr.responseText)
     //        })
     //
     //    }

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
                +"<td>"+item.status+"</td>"
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
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#date').val([year, month, day].join('-'));
    $('#resumeDate').val([year, month, day].join('-'));
    $('#classMvDate').val([year, month, day].join('-'));

}
function studentImage(url){
        $("#student-avatar").fileinput('destroy').fileinput({
            overwriteInitial: true,
            maxFileSize: 1500,
            showClose: false,
            showCaption: false,
            showBrowse: false,
            browseLabel: '',
            removeLabel: '',
            browseIcon: '',
            removeIcon: '',
            removeTitle: 'Cancel or reset changes',
            elErrorContainer: '#kv-avatar-errors',
            msgErrorClass: 'alert alert-block alert-danger',
            defaultPreviewContent: '<img src="' + url + '"  style="height:13em;width:230px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}
function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'67%',
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

function searchTableClass() {
        $('#table_search_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'75%',
            ajax: {
                delay: 250,
                url: 'searchtableclasses',
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

function searchNextMvClass() {
        $('#classmv_class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'100%',
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
function searchClassMvClass() {
        $('#nextmv_class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'100%',
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
            if(s[0].resumeDate) {
                $('#resumeDate').val(s[0].resumeDate);
            }
             if(s[0].action==='S'||s[0].action==='ES'){
                 $('#resume').show()
                 $('#noResume').hide()
             }
             else{
                 $('#resume').hide()
                 $('#noResume').show()
             }
             if(s[0].date) {
            $('#date').val(s[0].date);
            }
            $('#action').val(s[0].action);
            $('#reason').val(s[0].reason);
            $('#term').val(s[0].term);

            if (s[0].studentCode) {
                var $newCat = $("<option selected='selected' value='" + s[0].studentCode + "'>'+s[0].studentName+'</option>").val(s[0].studentCode.toString()).text(s[0].studentName)

                $('#student_frm').append($newCat).trigger('change');
                $('#studentCode').val(s[0].studentCode)
            }
            else {
                $('#student_frm').empty();
                $('#studentCode').val('')

            }


			if (s[0].classCode) {
			    var $newCl = $("<option selected='selected' value='" + s[0].classCode + "'>'+s[0].className+'</option>").val(s[0].classCode.toString()).text(s[0].className)

               $('#class_frm').append($newCl).trigger('change');
			    $('#classCode').val(s[0].classCode)
			    }
			    else {
			    $('#class_frm').empty();
			    $('#classCode').val('')

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


function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
        searchStudent(data.id)
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}

function getStudImage(id) {
     $.ajax({
          type: 'GET',
          url: 'getimage/'+id,
      }).done(function (s) {
          studentImage(s.url)
      }).fail(function (xhr, error) {
          bootbox.alert(xhr.responseText)

      });
}

function studentChange() {
    $('#student_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#studentCode').val(data.id)
         getStudImage(data.id)
    });
    $("#student_frm").on("select2:unselecting", function(e) {
    $('#studentCode').val('')
 });
}
function nextChange(){
     $('#nextmv_class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#nextMvClassCode').val(data.id)
         getLoaded()
    });
    $("#nextmv_class_frm").on("select2:unselecting", function(e) {
    $('#nextMvClassCode').val('')
 });
}
function moveChange(){
    $('#classmv_class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classmvClassCode').val(data.id)
        getUnloaded()
    });
    $("#classmv_class_frm").on("select2:unselecting", function(e) {
    $('#classmvClassCode').val('')
})
}

function tableSearchChange(){
    $('#table_search_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#sClass').val(data.id)
        getStudentsClass(data.id)
    });
    $("#table_search_frm").on("select2:unselecting", function(e) {
    $('#sClass').val('')
        getStudents()
})
}

function searchStudent(id){
     $('#student_frm').select2({
            placeholder: 'Students',
            allowClear: true,
            width:'67%',
            ajax: {
                delay: 250,
                url: 'searchstudent/'+id,
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
function getUnloaded(){
    var data = $('#classmvClassCode').val();
     $.ajax({
        type: 'GET',
        url: 'getunassignedstudents/'+data,

    }).done(function (s) {
       $('#unAssignedTbl').DataTable().destroy();
       $("#unAssignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#unAssignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="studCode" value="'+item.studentCode+'"><input type="checkbox" class="stud-check">&nbsp;&nbsp;'+item.name+"</td>"
                    + "</tr>")
            })
        }
        $('#unAssignedTbl').DataTable({
                        'dom': 't',
                         scrollY: "400px",
        });
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}
function getLoaded() {
  var data = $('#nextMvClassCode').val();
     $.ajax({
        type: 'GET',
        url: 'getassignedstudents/'+data,

    }).done(function (s) {
       $('#assignedTbl').DataTable().destroy();
       $("#assignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#assignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="studCode" value="'+item.studentCode+'"><input type="checkbox" class="stud-check">&nbsp;&nbsp;'+item.name+"</td>"
                    + "</tr>")
            })
        }
        $('#assignedTbl').DataTable({
            'dom': 't',
             scrollY: "400px"
        });
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}