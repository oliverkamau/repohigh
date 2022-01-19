$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
formatDate()
getDynamicUrl()
searchClass()
classChange()
getStudent()
getLeaveOutStudent()
assignLeaves()
unassignLeaves()
assignStudentLeaves()
unassignStudentLeaves()
    assignallStudentLeaveouts()
    unassignallStudentLeaveouts()
    getStudentsLeavesTable()
    editStudent()
    issueleaveouts()
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
function formatDate() {
    var d = new Date(),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    $('#leftDate').val([year, month, day].join('-'));
    $('#returnDate').val([year, month, day].join('-'));
    $('#returnedDate').val('');

}
function assignStudentLeaves() {
 $('#assignSelected').on('click',function (s) {
  if(assigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign leaves to',
         confirmButtonText: 'OK'
      })
  }
  else if($('#reason').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide reason to send student to leave',
         confirmButtonText: 'OK'
      })
  }
    else if($('#leftDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date to send student to leave',
         confirmButtonText: 'OK'
      })
  }
       else if($('#returnDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date for student to return',
         confirmButtonText: 'OK'
      })
  }
  else {
         swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
      var data = new FormData();
           data.append("classcode", $('#classCode').val())
           data.append("type", $('#leaveorreturn').val())
           data.append("leftdate", $('#leftDate').val())
           data.append("returndate", $('#returnDate').val())
           data.append("reason", $('#reason').val())
           data.append("returneddate", $('#returnedDate').val())
           data.append('students', JSON.stringify(assigned))
      var url = ''
      if(assigned.length===1 && $('#studentCode').val()!==''){
          url = 'assignleaveouts'
      }
      else{
          url = 'assignbulkleaves'
      }
      $.ajax({
          type: 'POST',
          url: url,
          data: data,
          processData: false,
          contentType: false,
      }).done(function (s) {
            swal.close()
          if(url==='assignleaveouts') {
              $('#studentCode').val(s.code)
              getStudent()
              getLeaveOutStudent()
          }
         else if(url==='assignbulkleaves'){
               getLoaded()
               getUnloaded()
          }
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

function assignallStudentLeaveouts() {
$('#assignAll').on('click',function (s) {
      if($('#classCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign leaves to',
         confirmButtonText: 'OK'
      })
  }else if($('#reason').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide reason to send student to leave',
         confirmButtonText: 'OK'
      })
  }
    else if($('#leftDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date to send student to leave',
         confirmButtonText: 'OK'
      })
  }
       else if($('#returnDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date for student to return',
         confirmButtonText: 'OK'
      })
  }
      else {
          swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
          var data = new FormData();
          data.append("classcode", $('#classCode').val())
          data.append("type", $('#leaveorreturn').val())
           data.append("leftdate", $('#leftDate').val())
           data.append("returndate", $('#returnDate').val())
           data.append("reason", $('#reason').val())
           data.append("returneddate", $('#returnedDate').val())
          $.ajax({
              type: 'POST',
              url: 'assignallleaveouts',
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



function unassignallStudentLeaveouts() {
$('#unAssignAll').on('click',function (s) {
     if($('#classCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign leaves to',
         confirmButtonText: 'OK'
      })
  }
       else if($('#returnedDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date  student returned',
         confirmButtonText: 'OK'
      })
  }
       else {
            swal({
              title: "Assigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
         var data = new FormData();
          data.append("classcode", $('#classCode').val())
           data.append("type", $('#leaveorreturn').val())
           data.append("leftdate", $('#leftDate').val())
           data.append("returndate", $('#returnDate').val())
           data.append("reason", $('#reason').val())
           data.append("returneddate", $('#returnedDate').val())
         $.ajax({
             type: 'POST',
             url: 'unassignallleaveouts',
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

function unassignStudentLeaves() {
 $('#unAssignSelected').on('click',function (s) {
       if(unassigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign subjects to',
         confirmButtonText: 'OK'
      })
  }
  else if($('#returnedDate').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'Provide date  student returned',
         confirmButtonText: 'OK'
      })
  }else {
              swal({
              title: "UnAssigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
           var data = new FormData();
           data.append("classcode", $('#classCode').val())
           data.append("type", $('#leaveorreturn').val())
           data.append("leftdate", $('#leftDate').val())
           data.append("returndate", $('#returnDate').val())
           data.append("reason", $('#reason').val())
           data.append("returneddate", $('#returnedDate').val())
           data.append('students', JSON.stringify(unassigned))
             var url = ''
      if(unassigned.length===1 && $('#studentCode').val()!==''){
          url = 'unassignleaveouts'
      }
      else{
          url = 'unassignbulkleaves'
      }
           $.ajax({
               type: 'POST',
               url: url,
               data: data,
               processData: false,
               contentType: false,
           }).done(function (s) {
            swal.close()
             if(url==='unassignleaveouts') {
              $('#studentCode').val(s.code)
              getStudent()
              getLeaveOutStudent()
          }
         else if(url==='unassignbulkleaves'){
               getLoaded()
               getUnloaded()
          }
            unassigned=[]

      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)
      });
       }
    });
}
function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class',
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

function assignLeaves() {
$('#unAssignedTbl').on('change','.stud-check',function (s) {

    var data=$(this).closest('tr').find('#studCode').val();

    if(this.checked){
    if(assigned.indexOf(data) === -1){
        console.log(data)
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

function unassignLeaves() {
$('#assignedTbl').on('change','.stud-check',function (s) {

    var data=$(this).closest('tr').find('#studCode').val();

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
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
        getUnloaded()
        getLoaded()
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function getUnloaded(){
    var data = $('#classCode').val();
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
            $('#studentCode').val('')
                        $('#leaveorreturn').val('')
           $('#assignAll').prop('disabled',false)
           $('#unAssignAll').prop('disabled',false)
        }
        $('#unAssignedTbl').DataTable({
                        'dom': 't',
                         scrollY: "400px",
        });
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}
function getStudent(){
    var data = $('#studentCode').val();
    if(data !== 'None') {
        $.ajax({
            type: 'GET',
            url: 'getindividualstudent/' + data,

        }).done(function (s) {
            $('#unAssignedTbl').DataTable().destroy();
            $("#unAssignedTbl tbody").empty();
            if (s.length !== 0) {
                $.each(s, function (i, item) {
                    $("#unAssignedTbl tbody").append(
                        "<tr scope='col'>"
                        + "<td>" + '<input type="hidden" id="studCode" value="' + item.studentCode + '"><input type="checkbox" class="stud-check">&nbsp;&nbsp;' + item.name + "</td>"
                        + "</tr>")
                })
                	if (s[0].class_name) {
			    var $newStat = $("<option selected='selected' value='" + s[0].class_code + "'>'+s[0].class_name+'</option>").val(s[0].class_code.toString()).text(s[0].class_name)

               $('#class_frm').append($newStat).trigger('change');
			   $('#classCode').val(s[0].class_code)

			    }
          	else {
			    $('#class_frm').empty();
			    $('#classCode').val('')

			}
          	            // $('#studentCode').val('')
          	          	$('#leaveorreturn').val('leave')
                        $('#assignAll').prop('disabled',true)
                        $('#unAssignAll').prop('disabled',true)

            }
            $('#unAssignedTbl').DataTable({
                'dom': 't',
                scrollY: "400px",
            });
        }).fail(function (xhr, error) {
            bootbox.alert(xhr.responseText);
        });
    }
}
function getLeaveOutStudent(){
    var data = $('#studentCode').val();
    if(data !== 'None') {
        $.ajax({
            type: 'GET',
            url: 'getindividualleavestudent/' + data,

        }).done(function (s) {
            $('#assignedTbl').DataTable().destroy();
            $("#assignedTbl tbody").empty();
            if (s.length !== 0) {

                $.each(s, function (i, item) {
                    $("#assignedTbl tbody").append(
                        "<tr scope='col'>"
                        + "<td>" + '<input type="hidden" id="studCode" value="' + item.studentCode + '"><input type="checkbox" class="stud-check">&nbsp;&nbsp;' + item.name + "</td>"
                        + "</tr>")
                })
                	if (s[0].class_name) {
			    var $newStat = $("<option selected='selected' value='" + s[0].class_code + "'>'+s[0].class_name+'</option>").val(s[0].class_code.toString()).text(s[0].class_name)

               $('#class_frm').append($newStat).trigger('change');
			   $('#classCode').val(s[0].class_code)

			    }
          	else {
			    $('#class_frm').empty();
			    $('#classCode').val('')

			}
          	$('#leaveorreturn').val('return')
            $('#studentCode').val(s[0].studentCode)
            $('#reason').val(s[0].reason)
            $('#returnDate').val(s[0].date_expected_back)
            $('#leftDate').val(s[0].date_left)
            $('#assignAll').prop('disabled',true)
            $('#unAssignAll').prop('disabled',true)

            }
            $('#assignedTbl').DataTable({
                'dom': 't',
                scrollY: "400px",
            });

        }).fail(function (xhr, error) {
            bootbox.alert(xhr.responseText);
        });
    }
}

function getLoaded() {
  var data = $('#classCode').val();
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
            $('#leaveorreturn').val('')
              $('#assignAll').prop('disabled',false)
           $('#unAssignAll').prop('disabled',false)
        }
        $('#assignedTbl').DataTable({
            'dom': 't',
             scrollY: "400px"
        });
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
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
            if(s[0].returned === 'Yes') {
                $('#leaveorreturn').val('leave')


            }
            else{
                $('#leaveorreturn').val('return')

            }
            $('#studentCode').val(s[0].studentCode)
            getStudent()
            getLeaveOutStudent()
            $('#reason').val(s[0].reason)
            $('#returnDate').val(s[0].dateExpected)
            $('#leftDate').val(s[0].dateLeft)
            $('#returnedDate').val(s[0].dateReturned)

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}

function getStudentsLeavesTable() {
     $.ajax({
        type: 'GET',
        url: 'getstudentsleaves',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#studTable').DataTable().destroy();
        $("#studTable tbody").empty();
        $.each(s,function(i,item){
            $("#studTable tbody").append(
                "<tr>"
                 +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-student" name="id" value='+item.leaveCode+'></form><button class="btn btn-outline-primary btn-sm btn-editstudent" ><i class="fa fa-edit"></button>'
                +"</td>"
                 +"<td>"+item.studentClass+"</td>"
                +"<td>"+item.admNo+"</td>"
                +"<td>"+item.name+"</td>"
                +"<td>"+item.reason+"</td>"
                +"<td>"+item.dateLeft+"</td>"
                +"<td>"+item.dateExpected+"</td>"
                +"<td>"+item.dateReturned+"</td>"
                +"<td>"+item.authorisedBy+"</td>"
                +"<td>"+item.returnedBy+"</td>"
                +"<td>"+item.returned+"</td>"
                +"</tr>" )
        })
        $('#studTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}

function issueleaveouts(){
    $('#back').click(function () {
      var url = '';
         if($('#entryStudent').val()==='') {
           url='getstudentsurl';
         }
         else{
             url='getstudenturl/'+$('#entryStudent').val();
         }
   $.ajax({
          type: 'GET',
          url: url,
      }).done(function (s) {
         window.location.replace(s.url);
      }).fail(function (xhr, error) {
          bootbox.alert(xhr.responseText)

      });


    })
}

