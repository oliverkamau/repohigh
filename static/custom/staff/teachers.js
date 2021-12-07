$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    teacherImage("");
    formatDate();
    searchTitle();
    titleChange();
    resChange();
    deptChange();
    searchResponsibility();
    searchDepartment();
    saveTeachers();
    getTeachers();
    editTeacher();
    deleteTeacher();
    $('#subjectsassignment').hide();
    $('#teacherregistry').show();
    checkregistry();
    checksubjects();
    assignSubjects();
    unassignSubjects();
    getDynamicUrl();
    assignTeacherSubjects();
    unassignTeacherSubjects();
    assignallSubjects();
    unassignallSubjects();
    unassignallSubjectsBtn();
    transferSubs();
    searchTeacher();
    transferChange();
    transferSubjects();
    newPage();
    searchClass();
    classChange();
})
function newPage(){
    $('#newTeacher').click(function () {
        clearpage();
    })
}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
         getSubjects();
          getSubjectsAssigned();
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function clearpage(){
    $('#teacher-form')[0].reset();
    $('#responsibility_frm').empty();
    $('#department_frm').empty();
    $('#title_frm').empty();
    $('#transfer_frm').empty();
    $('#teacherCode').val('');
    $('#titleCode').val('');
    $('#responsibilityCode').val('');
    $('#departmentCode').val('');
    $('#teacherTransferFrom').val('');
    $('#teacherTransferTo').val('');
    formatDate()

}
function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'75%',
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
function getSubjects() {
 var data = $('#teacherCode').val();
  var cl  = $('#classCode').val();

     $.ajax({
        type: 'GET',
        url: 'getunassignedsubjects/'+data+'/'+cl,

    }).done(function (s) {
       $('#unAssignedTbl').DataTable().destroy();
       $("#unAssignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#unAssignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="subCode" value="'+item.subjectCode+'"><input type="checkbox" class="sub-check">&nbsp;&nbsp;&nbsp;&nbsp;'+item.subjectName+ "</td>"
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

function assignSubjects() {
$('#unAssignedTbl').on('change','.sub-check',function (s) {

    var data=$(this).closest('tr').find('#subCode').val();

    if(this.checked){
    if(assigned.indexOf(data) === -1){
        assigned.push(data)
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
function transferSubs(){
    $('#transfer').on('click',function (s) {
        if($('#teacherCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Teacher selected to transfer subjects from',
         confirmButtonText: 'OK'
      })
  } else {

            $('#teacherTransferFrom').val($('#teacherCode').val());
            $('#teacherTransferName').val($('#teacherName').val());


            $('#transferModal').modal({backdrop: 'static', keyboard: false});
        }
    })


}
function assignTeacherSubjects() {
 $('#assignSelected').on('click',function (s) {
  if(assigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Subjects selected to assign',
         confirmButtonText: 'OK'
      })
  } else {
         swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
      var data = new FormData();
      data.append("teacher", $('#teacherCode').val());
      data.append('subjects', JSON.stringify(assigned));
      data.append("classcode", $('#classCode').val());

      $.ajax({
          type: 'POST',
          url: 'assignsubjects',
          data: data,
          processData: false,
          contentType: false,
      }).done(function (s) {
            swal.close()
          getSubjectsAssigned();
          getSubjects();
          assigned=[]
        // swal({
        //  type: 'success',
        //  title: 'Success',
        //  text: s.success,
        //  showConfirmButton: true,
     //})
      }).fail(function (xhr, error) {
            swal.close()
           getSubjectsAssigned();
          getSubjects();
          assigned=[]
          bootbox.alert(xhr.responseText)

      });
  }
    });

}
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
function unassignTeacherSubjects() {
 $('#unAssignSelected').on('click',function (s) {
       if(unassigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Subjects selected to unassign',
         confirmButtonText: 'OK'
      })
  } else {
              swal({
              title: "UnAssigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
           var data = new FormData();
           data.append("teacher", $('#teacherCode').val());
           data.append('subjects', JSON.stringify(unassigned));
           data.append("classcode", $('#classCode').val());

           $.ajax({
               type: 'POST',
               url: 'unassignsubjects',
               data: data,
               processData: false,
               contentType: false,
           }).done(function (s) {
            swal.close();
            getSubjectsAssigned();
            getSubjects();
            unassigned=[]

      }).fail(function (xhr, error) {
            swal.close()
               getSubjectsAssigned();
            getSubjects();
            unassigned=[]
              bootbox.alert(xhr.responseText)
      });
       }
    });
}

function unassignSubjects() {
$('#assignedTbl').on('change','.sub-check',function (s) {

    var data=$(this).closest('tr').find('#subCode').val();

    if(this.checked){
    if(unassigned.indexOf(data) === -1){
        unassigned.push(data)
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
function getSubjectsAssigned() {

    var data = $('#teacherCode').val();
    var cl =  $('#classCode').val();
     $.ajax({
        type: 'GET',
        url: 'getassignedsubjects/'+data+'/'+cl,

    }).done(function (s) {
       $('#assignedTbl').DataTable().destroy();
       $("#assignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#assignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="subCode" value="'+item.subjectCode+'"><input type="checkbox" class="sub-check">&nbsp;&nbsp;&nbsp;&nbsp;'+item.subjectName+ "</td>"
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

function assignallSubjects() {
$('#assignAll').on('click',function (s) {
      if($('#teacherCode').val()==='' ||  $('#classCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Teacher or class selected to assign subjects to',
         confirmButtonText: 'OK'
      })
  } else {
          swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
          var data = new FormData();
          data.append("teacher", $('#teacherCode').val());
          data.append("classcode", $('#classCode').val());

          $.ajax({
              type: 'POST',
              url: 'assignallsubjects',
              data: data,
              processData: false,
              contentType: false,
          }).done(function (s) {
              swal.close();
              getSubjects();
              getSubjectsAssigned();
      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)

      });
      }
    });
}
function unassignallSubjectsBtn() {
$('#unassignallbtn').on('click',function (s) {
     if($('#teacherCode').val() ==='' || $('#classCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Teacher or Class selected to assign subjects to',
         confirmButtonText: 'OK'
      })
  } else {
            swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
         var data = new FormData();
         data.append("teacher", $('#teacherCode').val());
         data.append("classcode", $('#classCode').val());
         data.append("classcode", $('#classCode').val());

         $.ajax({
             type: 'POST',
             url: 'unassignallsubjects',
             data: data,
             processData: false,
             contentType: false,
         }).done(function (s) {
            swal.close();
             getSubjects();
             getSubjectsAssigned();
      }).fail(function (xhr, error) {
          swal.close()
            bootbox.alert(xhr.responseText)


      });
     }
    });
}
function unassignallSubjects() {
$('#unAssignAll').on('click',function (s) {
     if($('#teacherCode').val()==='' || $('#classCode').val() === '')
{
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign subjects to',
         confirmButtonText: 'OK'
      })
  } else {
            swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
         var data = new FormData();
         data.append("teacher", $('#teacherCode').val());
         data.append("classcode", $('#classCode').val());

         $.ajax({
             type: 'POST',
             url: 'unassignallsubjects',
             data: data,
             processData: false,
             contentType: false,
         }).done(function (s) {
            swal.close();
             getSubjects();
             getSubjectsAssigned();
      }).fail(function (xhr, error) {
          swal.close()
            bootbox.alert(xhr.responseText)


      });
     }
    });
}
function checkregistry() {
$('#assign').on('change',function (s) {

    if(this.checked){
     $('#assign').prop('checked', false);

        if($('#teacherCode').val()===''){
             swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a teacher to assign subjects to!',
         confirmButtonText: 'OK'
      })

        }
        else {
            $('#assign').prop('checked', false);
            $('#assign-subs').prop('checked', true);
            $('#subjectsassignment').show()
            $('#teacherregistry').hide();
        }

    }
    else {
         $('#assign').prop('checked',true);
        $('#assign-subs').prop('checked',false);
        $('#subjectsassignment').hide()
        $('#teacherregistry').show();
    }
});


}
function transferSubjects(){
        $('#transferToBtn').click(function () {

         var transferTo=$('#teacherTransferTo').val();
         var transferFrom=$('#teacherTransferFrom').val();
         var data = new FormData();
         data.append("transferFrom",transferFrom );
         data.append("transferTo",transferTo);

         $.ajax({
             type: 'POST',
             url: 'transfersubjects',
             data: data,
             processData: false,
             contentType: false,
         }).done(function (s) {
             $('#transferModal').modal('hide');
                   swal({
         type: 'success',
         title: 'Success',
         text: s.success,
         showConfirmButton: true,
           })
      }).fail(function (xhr, error) {
            bootbox.alert(xhr.responseText)

      });

        })
}
function checksubjects() {
$('#assign-subs').on('change',function (s) {

    if(!this.checked){
        $('#assign').prop('checked',false);
        $('#assign-subs').prop('checked',true);
        $('#subjectsassignment').hide()
        $('#teacherregistry').show();
        $('#class_frm').empty();
        $('#classCode').val('');
         $('#unAssignedTbl tbody').empty();
         $('#assignedTbl tbody').empty();
    }
    else {
         $('#assign').prop('checked',true);
        $('#assign-subs').prop('checked',false);
        $('#subjectsassignment').show()
        $('#teacherregistry').hide();
    }
});


}
function revertTeacher(){
          $('#assign').prop('checked',false);
        $('#assign-subs').prop('checked',true);
        $('#subjectsassignment').hide()
        $('#teacherregistry').show();
        $('#class_frm').empty();
        $('#classCode').val('');
         $('#unAssignedTbl tbody').empty();
         $('#assignedTbl tbody').empty();
}
function titleChange() {
    $('#title_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#titleCode').val(data.id)
    });
    $("#title_frm").on("select2:unselecting", function (e) {
        $('#titleCode').val('')
    });
}
function resChange() {
    $('#responsibility_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#responsibilityCode').val(data.id)
    });
    $("#responsibility_frm").on("select2:unselecting", function(e) {
    $('#responsibilityCode').val('')
 });
}
function deptChange() {
    $('#department_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#departmentCode').val(data.id)
    });
    $("#department_frm").on("select2:unselecting", function(e) {
    $('#departmentCode').val('')
 });
}
function transferChange() {
    $('#transfer_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#teacherTransferTo').val(data.id)
    });
    $("#transfer_frm").on("select2:unselecting", function(e) {
    $('#teacherTransferTo').val('')
 });
}
function searchTitle() {
        $('#title_frm').select2({
            placeholder: 'Title',
            allowClear: true,
            width:'66%',
            ajax: {
                delay: 250,
                url: 'searchtitle',
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
function searchTeacher() {
        $('#transfer_frm').select2({
            placeholder: 'Teachers',
            allowClear: true,
            width: '100%',
            ajax: {
                delay: 250,
                url: 'searchteachers',
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
function searchResponsibility() {
        $('#responsibility_frm').select2({
            placeholder: 'Responsibilities',
            allowClear: true,
            width:'66%',
            ajax: {
                delay: 250,
                url: 'searchresponsibility',
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
function searchDepartment() {
        $('#department_frm').select2({
            placeholder: 'Departments',
            allowClear: true,
            width:'66%',
            ajax: {
                delay: 250,
                url: 'searchdepartment',
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
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#dateJoined').val([year, month, day].join('-'));
    $('#dateLeft').val([year, month, day].join('-'));

}
function teacherImage(url){
        $("#teacher-avatar").fileinput('destroy').fileinput({
            overwriteInitial: true,
            maxFileSize: 1500,
            showClose: false,
            showCaption: false,
            showBrowse: true,
            browseLabel: '',
            removeLabel: '',
            browseIcon: '<i class="fa fa-folder-open"></i>',
            removeIcon: '',
            removeTitle: 'Cancel or reset changes',
            elErrorContainer: '#kv-avatar-errors',
            msgErrorClass: 'alert alert-block alert-danger',
            defaultPreviewContent: '<img src="' + url + '"  style="height:15em;width:225px">',
            layoutTemplates: {main2: '{preview} ' + ' {remove} {browse}'},
            allowedFileExtensions: ["jpg", "png", "gif"]
        });

}
function saveTeachers(){
    $('#saveTeacher').click(function () {

        if($('#titleCode').val()==''){
         swal({
          title: 'Alert!',
          type: 'info',
          text: 'Title Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
        else if($('#teacherName').val()==='') {
            swal({
                title: 'Alert!',
                type: 'info',
                text: 'Teacher Name Field is Mandatory',
                confirmButtonText: 'OK'
            })
        }
         else if($('#responsibilityCode').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Responsibility Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#status').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Status Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#address').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Address Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#phoneNumber').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Telephone Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#email').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Email Address Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#idNo').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'ID Number Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#tscNo').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'TscNo/UPI Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }
         else if($('#intials').val()===''){
           swal({
          title: 'Alert!',
          type: 'info',
          text: 'Teacher Intials Field is Mandatory',
         confirmButtonText: 'OK'
      })
        }

        else {
            var form = $("#teacher-form")[0];
            var data = new FormData(form);
            data.append('teacher_pic', $('#teacher-avatar')[0].files[0]);
            var url = '';
            if ($('#teacherCode').val() === '') {
                url = 'addteachers'
            } else {
                url = 'updateteachers/' + $('#teacherCode').val()
            }
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                processData: false,
                contentType: false
            }).done(function (s) {
                clearpage();
                getTeachers()
                swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })

            }).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
                // bootbox.alert("Error Occured while saving")
            })

        }
	})
}
function getTeachers() {
     $.ajax({
        type: 'GET',
        url: 'getteachers',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#teaTable').DataTable().destroy();
       $("#teaTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#teaTable tbody").append(
                    "<tr scope='col'>"
                    + "<td>" + item.name + "</td>"
                    + "<td>" + item.gender + "</td>"
                    + "<td>" + item.phone + "</td>"
                    + "<td>" + item.email + "</td>"
                   + "<td>" + item.address + "</td>"
                    + "<td>" + item.responsibility + "</td>"
                      + "<td>" + item.admDate + "</td>"
                    + "<td>" + item.tscNo + "</td>"
                     + "<td>" + item.staffNo + "</td>"
                    + "<td>" + item.idNo + "</td>"
                    + "<td>" + item.department + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-teacher" name="id" value=' + item.teacherCode + '></form><button class="btn btn-outline-primary btn-sm btn-editTeacher" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-teacher" name="id" value=' + item.teacherCode + '></form><button class="btn btn-outline-danger btn-sm btn-deleteTeacher" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#teaTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function deleteTeacher() {
     $('#teaTable').on('click','.btn-deleteTeacher',function (s) {
        var data = $(this).closest('tr').find('#delete-teacher').val();
        bootbox.confirm("Are you sure want to delete this Teacher?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteteacher/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          getTeachers()
          swal({
                    type: 'success',
                    title: 'Success',
                    text: s.success,
                    showConfirmButton: true
                })

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function editTeacher(){
    $('#teaTable').on('click','.btn-editTeacher',function (s) {
        var data=$(this).closest('tr').find('#edit-teacher').val();
        $.ajax({
            type: 'GET',
            url: 'editteacher/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#teacherCode').val(s.teacher_code);
            $('#teacherName').val(s.teacher_name);
            $('#gender').val(s.gender);
            $('#status').val(s.status);
            $('#address').val(s.box_address);
            $('#dateJoined').val(s.date_joined);
            $('#dateLeft').val(s.date_left);
            $('#tscNo').val(s.tsc_no);
            $('#phoneNumber').val(s.phone_number);
            $('#email').val(s.email);
            $('#idNo').val(s.id_no);
            $('#intials').val(s.intials);

            if (s.title_code) {
                var $newCat = $("<option selected='selected' value='" + s.title_code + "'>'+s.title_name+'</option>").val(s.title_code.toString()).text(s.title_name)

                $('#title_frm').append($newCat).trigger('change');
                $('#titleCode').val(s.title_code)
            }
            else {
                $('#title_frm').empty();
                $('#titleCode').val('')

            }

			if (s.rb_code) {
			    var $newDorm= $("<option selected='selected' value='" + s.rb_code + "'>'+s.rb_name+'</option>").val(s.rb_code.toString()).text(s.rb_name)

               $('#responsibility_frm').append($newDorm).trigger('change');
			    $('#responsibilityCode').val(s.rb_code)
			    }
			    else {
			    $('#responsibility_frm').empty();
			    $('#responsibilityCode').val('')

			}
			if (s.dp_code) {
			    var $newCam = $("<option selected='selected' value='" + s.dp_code + "'>'+s.dp_name+'</option>").val(s.dp_code.toString()).text(s.dp_name)

               $('#department_frm').append($newCam).trigger('change');
			    $('#departmentCode').val(s.dp_code)
			    }
			    else {
			    $('#department_frm').empty();
			    $('#departmentCode').val('')

			}
			if(s.url) {
                teacherImage(s.url)
            }
            else{
			    teacherImage("")
            }
            revertTeacher()

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}