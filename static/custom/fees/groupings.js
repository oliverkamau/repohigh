$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
searchFeeCategory()
searchNewFeeCategory()
searchClass()
classChange()
feeChange()
newFeeChange()
assignCategory()
unassignCategory()
unassignallCategory()
assignallCategory()
assignStudentCategory()
unassignStudentCategory()
getDynamicUrl()
updateGroup()
})
function updateGroup() {
$('#update').click(function () {
 swal({
                    type: 'success',
                    title: 'Success',
                    text: 'Assigned Successfully!',
                    showConfirmButton: true
                })
})
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

function searchNewFeeCategory() {
     $('#new_fee_frm').select2({
           placeholder: 'Fees',
           allowClear: true,
           ajax: {
             delay: 250,
             url: 'searchnewfeecategory',
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

function searchClass() {

        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            ajax: {
                delay: 250,
                url: 'searchclass',
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
         searchFeeStudent()
          if($('#newCategoryCode').val()!==''){
           searchNewFeeStudent()
        }
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')

 });
}

function feeChange() {
    $('#fee_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#categoryCode').val(data.id)
        searchFeeStudent()
        if($('#newCategoryCode').val()!==''){
           searchNewFeeStudent()
        }
    });
    $("#fee_frm").on("select2:unselecting", function(e) {
    $('#categoryCode').val('')
 });
}

function newFeeChange() {
    $('#new_fee_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#newCategoryCode').val(data.id)
    });
    $("#new_fee_frm").on("select2:unselecting", function(e) {
    $('#newCategoryCode').val('')
 });
}

// function searchClassStudent() {
// var data = $('#classCode').val();
//      $.ajax({
//         type: 'GET',
//         url: 'getclassstudents/'+data,
//
//     }).done(function (s) {
//        $('#unAssignedTbl').DataTable().destroy();
//        $("#unAssignedTbl tbody").empty();
//         if(s.length!==0) {
//             $.each(s, function (i, item) {
//                 $("#unAssignedTbl tbody").append(
//                     "<tr scope='col'>"
//                      + "<td>" + '<input type="hidden" id="studCode" value="'+item.studentCode+'"><input type="checkbox" class="stud-check">&nbsp;&nbsp;&nbsp;&nbsp;'+item.name+ "</td>"
//                     + "</tr>")
//             })
//         }
//         $('#unAssignedTbl').DataTable({
//             'dom': 't',
//              scrollY: "400px"
//         });
//     }).fail(function (xhr, error) {
//        bootbox.alert(xhr.responseText);
//     });
// }

function searchFeeStudent() {
 var data = $('#categoryCode').val();
 var classcode = $('#classCode').val();
 var url = ''
 if(classcode !== '' && data !== ''){
     url='getfeestudents/'+data+'/'+classcode
 }
 else if(data !== '' && classcode ===''){
     url='getfeestudent/'+data
 }
 else if(data === '' && classcode !==''){
             url = 'getclassstudents/'+classcode
 }
     $.ajax({
        type: 'GET',
        url: url,

    }).done(function (s) {
       $('#unAssignedTbl').DataTable().destroy();
       $("#unAssignedTbl tbody").empty();
       // searchNewFeeStudent()
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
function searchNewFeeStudent() {
 var classcode = $('#classCode').val();
 var data = $('#newCategoryCode').val();
 var url = ''
 if(classcode !== '' && data !== ''){
     url='getnewfeestudents/'+data+'/'+classcode
 }
 else if(data !== '' && classcode ===''){
     url='getnewfeestudent/'+data
 }
     $.ajax({
        type: 'GET',
        url: url,

    }).done(function (s) {
       $('#assignedTbl').DataTable().destroy();
       $("#assignedTbl tbody").empty();
       // searchFeeStudent()
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
                         scrollY: "400px",
        });
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });
}
function assignStudentCategory() {
 $('#assignSelected').on('click',function (s) {
  if(assigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign category to',
         confirmButtonText: 'OK'
      })

  }
  else if($('#newCategoryCode').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Category selected to assign Students to',
         confirmButtonText: 'OK'
      })
  }
    else if($('#newCategoryCode').val()===$('#categoryCode').val()){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a different Category to assign to!',
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
      data.append("category", $('#categoryCode').val())
      data.append("newcategory", $('#newCategoryCode').val())
      data.append('students', JSON.stringify(assigned))
      $.ajax({
          type: 'POST',
          url: 'assigncategory',
          data: data,
          processData: false,
          contentType: false,
      }).done(function (s) {
          if(s.success) {
              swal.close()
              searchFeeStudent()
              searchNewFeeStudent()
              assigned = []
          }
           else if(s.timeout){
                        swal({
                        title: 'Alert!',
                       type: 'info',
                       text: s.timeout,
                        confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
              else{
                       swal({
                        title: 'Alert!',
                       type: 'info',
                       text: 'Your User Session expired!',
                        confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
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
function unassignStudentCategory() {
 $('#unAssignSelected').on('click',function (s) {
       if(unassigned.length===0){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No students selected to assign subjects to',
         confirmButtonText: 'OK'
      })
  } else if($('#newCategoryCode').val()==='' || $('#categoryCode').val()===''){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Category selected to assign Students to and from',
         confirmButtonText: 'OK'
      })
  }
           else if($('#newCategoryCode').val()===$('#categoryCode').val()){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a different Category to assign to!',
         confirmButtonText: 'OK'
      })
  }
       else {
              swal({
              title: "UnAssigning...",
              imageUrl: spinner,
              showConfirmButton: false,
              allowOutsideClick: false
            });
           var data = new FormData();
           data.append("classcode", $('#classCode').val())
           data.append("category", $('#categoryCode').val())
           data.append("newcategory", $('#newCategoryCode').val())
           data.append('students', JSON.stringify(unassigned))
           $.ajax({
               type: 'POST',
               url: 'unassigncategory',
               data: data,
               processData: false,
               contentType: false,
           }).done(function (s) {
            swal.close()
          searchFeeStudent()
          searchNewFeeStudent()
            unassigned=[]

      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)
      });
       }
    });
}
function assignallCategory() {
$('#assignAll').on('click',function (s) {
      if($('#newCategoryCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Category to move to Selected!',
         confirmButtonText: 'OK'
      })
  }
          else if($('#newCategoryCode').val()===$('#categoryCode').val()){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a different Category to assign to!',
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
          data.append("category", $('#categoryCode').val())
          data.append("newcategory", $('#newCategoryCode').val())
          $.ajax({
              type: 'POST',
              url: 'assignallcategories',
              data: data,
              processData: false,
              contentType: false,
          }).done(function (s) {
              if(s.success) {
                  swal.close()
                  searchFeeStudent()
                  searchNewFeeStudent()
              }
                  else if(s.timeout){
                        swal({
                        title: 'Alert!',
                       type: 'info',
                       text: s.timeout,
                        confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
                    else{
                       swal({
                        title: 'Alert!',
                       type: 'info',
                       text: 'Your User Session expired!',
                        confirmButtonText: 'OK'
                      })
                       setInterval('refreshPage()', 3 * 1000);
                    }
      }).fail(function (xhr, error) {
            swal.close()
              bootbox.alert(xhr.responseText)

      });
      }
    });
}
function refreshPage() {

    window.location.reload()

    }
function unassignallCategory() {
$('#unAssignAll').on('click',function (s) {
      if($('#categoryCode').val()===''){
      swal({
          title: 'Alert!',
          type: 'info',
          text: 'No Category to move to Selected!',
         confirmButtonText: 'OK'
      })
  }
          else if($('#newCategoryCode').val()===$('#categoryCode').val()){
       swal({
          title: 'Alert!',
          type: 'info',
          text: 'Select a different Category to assign to!',
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
          data.append("category", $('#categoryCode').val())
          data.append("newcategory", $('#newCategoryCode').val())
         $.ajax({
             type: 'POST',
             url: 'unassignallcategories',
             data: data,
             processData: false,
             contentType: false,
         }).done(function (s) {
            swal.close()
          searchFeeStudent()
          searchNewFeeStudent()
      }).fail(function (xhr, error) {
          swal.close()
            bootbox.alert(xhr.responseText)


      });
     }
    });
}
function assignCategory() {
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

function unassignCategory() {
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

