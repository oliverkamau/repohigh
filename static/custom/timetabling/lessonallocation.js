$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
searchClass();
classChange();
searchDays();
dayChange();
searchLesson();
lessonChange();
searchSubject();
subjectChange();
searchTeachers();
teacherChange();
getCurrentTerm();
newTimeTable();
saveTimetable();
getTimetable();
 })

function newTimeTable(){
$('#newTimetable').click(function(){
clearData();
})
}
function getCurrentTerm(){
$.ajax({
			type: 'GET',
			url: 'getcurrentterm',
		}).done(function (s) {
            $('#term').text(s.termNumber)
            $('#termNumber').val(s.termCode)

		}).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
		})

}
function deleteLesson() {
    $('#lessonTable').on('click','.btn-deleteLesson',function (s) {
        var data = $(this).closest('tr').find('#delete-lesson').val();
        bootbox.confirm("Are you sure want to delete this Lesson?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deletelesson/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {

         	     swal({
             type: 'success',
             title: 'Success',
             text: s.success,
             showConfirmButton: true
                        })
             getLessons()

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#ttClass').val(data.id)
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#ttClass').val('')
 });
}
function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Class',
            allowClear: true,
            width:'70%',
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

function dayChange() {
    $('#day_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#ttDay').val(data.id)
    });
    $("#day_frm").on("select2:unselecting", function(e) {
    $('#ttDay').val('')
 });
}
function searchDays() {

        $('#day_frm').select2({
            placeholder: 'Day',
            allowClear: true,
            width:'70%',
            ajax: {
                delay: 250,
                url: 'searchdays',
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

function lessonChange() {
    $('#lesson_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#ttLesson').val(data.id)
    });
    $("#lesson_frm").on("select2:unselecting", function(e) {
    $('#ttLesson').val('')
 });
}
function searchLesson() {

        $('#lesson_frm').select2({
            placeholder: 'Lesson',
            allowClear: true,
            width:'70%',
            ajax: {
                delay: 250,
                url: 'searchlessons',
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

function subjectChange() {
    $('#subject_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#ttSubject').val(data.id)
         var classes = $('#ttClass').val();
    if( classes !== ''){
     getTeacher(classes,data.id);
    }
    });
    $("#subject_frm").on("select2:unselecting", function(e) {
    $('#ttSubject').val('')

 });
}
function getTeacher(code,subject){
$.ajax({
			type: 'GET',
			url: 'getteacher/'+code+'/'+subject,
		}).done(function (s) {
            $('#ttTeacherName').val(s.teacherName)
            $('#ttTeacher').val(s.teacherCode)

		}).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
		})

}
function searchSubject() {

        $('#subject_frm').select2({
            placeholder: 'Subject',
            allowClear: true,
            width:'67%',
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

function teacherChange() {
    $('#teacher_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#ttTeacher').val(data.id)
    });
    $("#teacher_frm").on("select2:unselecting", function(e) {
    $('#ttTeacher').val('')
 });
}
function searchTeachers() {

        $('#teacher_frm').select2({
            placeholder: 'Teacher',
            allowClear: true,
            width:'70%',
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

function saveTimetable(){
    $('#saveTimetable').click(function () {
     if($('#ttDay').val()==='') {
             swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'Provide a Day for timetable setups!',
                 confirmButtonText: 'OK'
             })
         }
         else if($('#ttClass').val()===''){
          swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'Provide a Class for timetable setups!',
                 confirmButtonText: 'OK'
             })

         }
         else if($('#ttLesson').val()===''){
          swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'Provide a Lesson for timetable setups!',
                 confirmButtonText: 'OK'
             })

         }

         else if($('#ttSubject').val()===''){

          swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'Provide a Subject for timetable setups!',
                 confirmButtonText: 'OK'
             })
         }
              else if($('#ttTeacher').val()===''){

          swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'This subject has no teacher assigned to it in the selected class!',
                 confirmButtonText: 'OK'
             })
         }
         else{


        var data=$('#timetable-form').serialize();
        var url = '';
        if($('#timetableCode').val()===''){
          url = 'createtimetable'
        }
        else{
            url = 'updatetimetable/'+$('#timetableCode').val()
        }
		$.ajax({
			type: 'POST',
			url: url,
            data: data
		}).done(function (s) {
		     swal({

             type: 'success',
             title: 'Success',
             text: s.success,
             showConfirmButton: true

                        })
             clearData()
             getTimetable()
            $('#lessonModal').modal('hide')
		}).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
		})
   }

	})
}
function editLesson(){
    $('#lessonTable').on('click','.btn-editLesson',function (s) {
        var data=$(this).closest('tr').find('#edit-lesson').val();
        $.ajax({
            type: 'GET',
            url: 'editlesson/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#lessonCode').val(s.lesson_code);
            $('#lessonName').val(s.lesson_name);
             $('#lessonStart').attr({'value': s.lesson_start});
             $('#lessonEnd').attr({'value': s.lesson_end});

            if (s.lesson_auto === true) {
                $('#auto').prop('checked', true);
            }
            else {
                $('#auto').prop('checked', false);

            }
            $('#lessonModal').modal({backdrop: 'static', keyboard: false})
            }).fail(function (xhr, error) {

        bootbox.alert(xhr.responseText)
        });
    });

}

function clearData(){

 $('#timetableCode').val('');
 $('#ttDay').val('');
 $('#day_frm').empty();
 $('#ttClass').val('')
 $('#class_frm').empty();
 $('#ttLesson').val('')
 $('#lesson_frm').empty();
 $('#ttSubject').val('')
 $('#subject_frm').empty();
 $('#ttTeacher').val('')
 $('#teacher_frm').empty();

}
function getTimetable() {

     $.ajax({
        type: 'GET',
        url: 'getTimetable',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#timetableTable').DataTable().destroy();
       $("#timetableTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#timetableTable tbody").append(
                    "<tr>"
                       + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-lesson" name="id" value=' + item.code + '></form><button class="btn btn-outline-primary btn-sm btn-editLesson" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-lesson" name="id" value=' + item.code + '></form><button class="btn btn-outline-danger btn-sm btn-deleteLesson" ><i class="fa fa-trash-o"></button>'
                    + "</td>"
                    + "<td>" + item.lessonName + "</td>"
                    + "<td>" + item.subjectName + "</td>"
                    + "<td>" + item.dayName + "</td>"
                    + "<td>" + item.className + "</td>"
                    + "<td>" + item.termName + "</td>"
                    + "<td>" + item.teacherName + "</td>"


                    + "</tr>")
            })
        }
        $('#timetableTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}