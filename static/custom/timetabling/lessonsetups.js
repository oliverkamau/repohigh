$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
    formatTime();
    newLesson();
    deleteLesson();
    saveLesson();
    editLesson();
    getLessons();
    getDifference();

 })
 function formatTime(){

   var d = new Date(),
      h = d.getHours(),
      m = d.getMinutes();
//      s = d.getSeconds()
  if(h < 10) h = '0' + h;
  if(m < 10) m = '0' + m;
  s = '00';
  $('input[type="time"][value="now"]').each(function(){
    $(this).attr({'value': h + ':' + m + ':'+ s});
  });
 }
 function getDifference(){
 $('#lessonEnd').change(function (){

 var start = $('#lessonStart').val(),
 end = $('#lessonEnd').val(),
 hours = end.split(':')[0] - start.split(':')[0],
 minutes = end.split(':')[1] - start.split(':')[1];

    minutes = minutes.toString().length<2?'0'+minutes:minutes;
    if(minutes<0){
        hours--;
        minutes = 60 + minutes;
    }
    hours = hours.toString().length<2?'0'+hours:hours;
    var time=parseInt(hours)*60
    time = time + parseInt(minutes)
    console.log(time)
    $('#duration').val(time)

 })

 }
 function newLesson(){
$('#open-modal').click(function(){
console.log('in this already...')
clearData();
$('#lessonModal').modal({backdrop: 'static', keyboard: false})
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


function saveLesson(){
    $('#saveLesson').click(function () {
    if($('#lessonName').val()===''){
     swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'Provide a Lesson Name to Save!',
                 confirmButtonText: 'OK'
             })
    }
    else if(parseInt($('#duration').val()) > 40){
     swal({
                 title: 'Alert!',
                 type: 'info',
                 text: 'No Lesson should exceed 40 Minutes!',
                 confirmButtonText: 'OK'
             })
    }
    else{
        var data=$('#lesson-form').serialize();
        var url = '';
        if($('#lessonCode').val()===''){
          url = 'createlesson'
        }
        else{
            url = 'updatelesson/'+$('#lessonCode').val()
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
             getLessons()
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
             $('#type').val(s.lesson_type);
             $('#duration').val(s.lesson_duration);

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

      $('#lessonCode').val('');
      $('#lesson-form')[0].reset();
      $('#auto').prop('checked', false);
      formatTime();
}
function getLessons() {

     $.ajax({
        type: 'GET',
        url: 'getlessons',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#lessonTable').DataTable().destroy();
       $("#lessonTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#lessonTable tbody").append(
                    "<tr>"
                    + "<td>" + item.lesson_start + "</td>"
                    + "<td>" + item.lesson_end + "</td>"
                    + "<td>" + item.lesson_name + "</td>"
                    + "<td>" + item.lesson_auto + "</td>"

                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-lesson" name="id" value=' + item.lesson_code + '></form><button class="btn btn-outline-primary btn-sm btn-editLesson" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-lesson" name="id" value=' + item.lesson_code + '></form><button class="btn btn-outline-danger btn-sm btn-deleteLesson" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#lessonTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}