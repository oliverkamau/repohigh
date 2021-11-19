

$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    console.log($('[name=csrfmiddlewaretoken]').val())
    getDynamicUrl();
    searchClass();
    classChange();
    subjectChange();
    assignSubjects();
    unassignSubjects();
    assignStudentSubjects();
    unassignStudentSubjects();
    assignallStudentSubjects();
    unassignallStudentSubjects();
    mandatorypopulate()
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
function mandatorypopulate() {
     $('#assignMandatory').on('click',function (s) {
         $.ajax({
             type: 'GET',
             url: 'populatemandatorysubjects',
         }).done(function (s) {
             sweetAlert({
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
function assignStudentSubjects() {
 $('#assignSelected').on('click',function (s) {
  if(assigned.length===0){
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
      data.append("classcode", $('#classCode').val())
      data.append("subject", $('#subjectCode').val())
      data.append('students', JSON.stringify(assigned))
      $.ajax({
          type: 'POST',
          url: 'assignsubjects',
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
function unassignStudentSubjects() {
 $('#unAssignSelected').on('click',function (s) {
       if(unassigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign subjects to',
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
           data.append("classcode", $('#classCode').val())
           data.append("subject", $('#subjectCode').val())
           data.append('students', JSON.stringify(unassigned))
           $.ajax({
               type: 'POST',
               url: 'unassignsubjects',
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
function assignallStudentSubjects() {
$('#assignAll').on('click',function (s) {
      if($('#classCode').val()==='' || $('#subjectCode').val()===''){
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
          data.append("classcode", $('#classCode').val())
          data.append("subject", $('#subjectCode').val())
          $.ajax({
              type: 'POST',
              url: 'assignallsubjects',
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
function unassignallStudentSubjects() {
$('#unAssignAll').on('click',function (s) {
     if($('#classCode').val()==='' || $('#subjectCode').val()===''){
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
         data.append("classcode", $('#classCode').val())
         data.append("subject", $('#subjectCode').val())
         $.ajax({
             type: 'POST',
             url: 'unassignallsubjects',
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
function assignSubjects() {
$('#unAssignedTbl').on('change','.stud-check',function (s) {

    var data=$(this).closest('tr').find('#studCode').val();

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
function unassignSubjects() {
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

function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Select Class',
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
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)

        // console.log('country is: '+$('#country-id').val())
        searchSubjects()

    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function subjectChange() {
    $('#subject_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subjectCode').val(data.id)
        getUnloaded()
        getLoaded()
    });
    $("#subject_frm").on("select2:unselecting", function(e) {
    $('#subjectCode').val('')
 });
}
function searchSubjects() {
        $('#subject_frm').select2({
            placeholder: 'Select Subject',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchsubjects',
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
    var data = $('#classCode').val();
    var subject = $('#subjectCode').val()
     $.ajax({
        type: 'GET',
        url: 'getunassignedstudents/'+data+'/'+subject,

    }).done(function (s) {
       $('#unAssignedTbl').DataTable().destroy();
       $("#unAssignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#unAssignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="studCode" value="'+item.studentCode+'"><input type="checkbox" class="stud-check">&nbsp;&nbsp;&nbsp;&nbsp;'+item.name+ "</td>"
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
  var data = $('#classCode').val();
    var subject = $('#subjectCode').val()
     $.ajax({
        type: 'GET',
        url: 'getassignedstudents/'+data+'/'+subject,

    }).done(function (s) {
       $('#assignedTbl').DataTable().destroy();
       $("#assignedTbl tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#assignedTbl tbody").append(
                    "<tr scope='col'>"
                     + "<td>" + '<input type="hidden" id="studCode" value="'+item.studentCode+'"><input type="checkbox" class="stud-check">&nbsp;&nbsp;&nbsp;&nbsp;'+item.name+ "</td>"
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