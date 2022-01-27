
$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });
    // classModal();
    // getClasses();
    // saveClass();
    // editClass();
    // deleteClass();
    // searchClasses();
    // searchTeacher();
    // teacherChange();
    // classChange();
    // deleteClass();
      $('#sidebarCollapse').on('click',function () {
       $('#sidebar').toggleClass('active');
   })
    // autorefresh()
})
// function autorefresh() {
//  localStorage.removeItem("timer");
// console.log(localStorage.getItem("timer"))
// if (localStorage.getItem("timer") === null) {
//     localStorage.setItem("timer","set");
//     $.ajax({
//
//         type: 'GET',
//         url: 'getrefreshtime'
//
//     }).done(function (s) {
//          localStorage.removeItem("timer");
//         setInterval('refreshPage()', s.session * 1000);
//
//     }).fail(function (xhr, error) {
//         bootbox.alert(xhr.responseText)
//     });
//
// }
//     }




function classModal() {
    $('#open-modal').click(function () {
        clearData()
        $('#classModal').modal({backdrop: 'static', keyboard: false})
    })

}
function clearData(){
      $('#teacher-frm').empty();
      $('#class-frm').empty();
      $('#teacher-id').val('');
      $('#next-id').val('');
      $('#class-form')[0].reset();
      $('#classCode').val('');
}
function deleteClass() {
    $('#classTable').on('click','.btn-deleteClass',function (s) {
        var data = $(this).closest('tr').find('#delete-class').val();
        bootbox.confirm("Are you sure want to delete this Class?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteclasses/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          bootbox.hideAll()
          getClasses()
          bootbox.alert(s.success)


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}

function getClasses() {
     $.ajax({
        type: 'GET',
        url: 'getclasses',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#classTable').DataTable().destroy();
       $("#classTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#classTable tbody").append(
                    "<tr scope='col'>"
                    + "<td>" + item.className + "</td>"
                    + "<td>" + item.nextClass + "</td>"
                    + "<td>" + item.classTeacher + "</td>"
                    + "<td>" + item.maxCapacity + "</td>"
                    + "<td>" + item.currentCapacity + "</td>"
                    + "<td>" + item.status + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-class" name="id" value=' + item.classCode + '></form><button class="btn btn-outline-primary btn-sm btn-editClass" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-class" name="id" value=' + item.classCode + '></form><button class="btn btn-outline-danger btn-sm btn-deleteClass" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#classTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}

function saveClass(){
    $('#saveClass').click(function () {
        var data=$('#class-form').serialize();
        var url = '';
        if($('#classCode').val()===''){
          url = 'createclass'
        }else{
            url = 'updateclasses/'+$('#classCode').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data
		}).done(function (s) {
		    getClasses()
            clearData()
            $('#classModal').modal('hide')
			bootbox.alert(s.success)

		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})


	})
}
function editClass(){
    $('#classTable').on('click','.btn-editClass',function (s) {
        var data=$(this).closest('tr').find('#edit-class').val();
        $.ajax({
            type: 'GET',
            url: 'editclasses/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#classCode').val(s.classCode);
            $('#form').val(s.form);
            $('#stream').val(s.stream);
            $('#className').val(s.className);
            if (s.active === true) {
                $('#active').prop('checked', true);
            }
            else {
                $('#active').prop('checked', true);

            }
            $('#maxCapacity').val(s.maxCapacity);
            $('#currentCapacity').val(s.currentCapacity);
            $('#admnoPrefix').val(s.admnoPrefix);
            $('#county-frm').select2();
            if (s.nextClassCode) {
                $('#next-id').val(s.nextClassCode)
                var $newClass = $("<option selected='selected' value='" + s.nextClassCode + "'>'+s.nextClassName+'</option>").val(s.nextClassCode.toString()).text(s.nextClassName)

                $('#class-frm').append($newClass).trigger('change');
            }
            else {
                $('#next-id').val('')
                $('#class-frm').empty();
            }
            if (s.classTeacherCode) {
                $('#teacher-id').val(s.classTeacherCode)

                var $newOption = $("<option selected='selected' value='" + s.classTeacherCode + "'>'+s.classTeacherName+'</option>").val(s.classTeacherCode.toString()).text(s.classTeacherName)

                $('#teacher-frm').append($newOption).trigger('change');
            } else {
                $('#teacher-id').val('')

                $('#teacher-frm').empty();

            }

        $('#classModal').modal({backdrop: 'static', keyboard: false})
        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function searchTeacher() {
     $('#teacher-frm').select2({
           placeholder: 'Teachers',
           allowClear: true,
           width: '100%' ,
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
function searchClasses() {
     $('#class-frm').select2({
           placeholder: 'Classes',
           allowClear: true,
           width: '100%' ,
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
function teacherChange(){
    $('#teacher-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#teacher-id').val(data.id)
    $('#teacher-name').val(data.text)

});
    $("#teacher-frm").on("select2:unselecting", function(e) {
    $('#teacher-id').val('')
    $('#teacher-name').val('')
 });
}
function classChange(){
    $('#class-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#next-id').val(data.id)
    $('#next-name').val(data.text)

});
    $("#class-frm").on("select2:unselecting", function(e) {
    $('#next-id').val('')
    $('#next-name').val('')
 });
}
