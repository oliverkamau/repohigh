$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
    saveDay();
    newDay();
    getDays();
    editDay();
    deleteDay();
    formatTime();

 })

function newDay(){
$('#open-modal').click(function(){
console.log('in this already...')
clearData();
$('#dayModal').modal({backdrop: 'static', keyboard: false})
})
}
function deleteDay() {
    $('#dayTable').on('click','.btn-deleteDay',function (s) {
        var data = $(this).closest('tr').find('#delete-day').val();
        bootbox.confirm("Are you sure want to delete this Day?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteday/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {

         	     swal({
             type: 'success',
             title: 'Success',
             text: s.success,
             showConfirmButton: true
                        })
             getDays()

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}


function saveDay(){
    $('#saveDay').click(function () {
        var data=$('#day-form').serialize();
        var url = '';
        if($('#dayCode').val()===''){
          url = 'createday'
        }
        else{
            url = 'updateday/'+$('#dayCode').val()
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
             getDays()
            $('#dayModal').modal('hide')
		}).fail(function (xhr, error) {
                bootbox.alert(xhr.responseText)
		})


	})
}
function editDay(){
    $('#dayTable').on('click','.btn-editDay',function (s) {
        var data=$(this).closest('tr').find('#edit-day').val();
        $.ajax({
            type: 'GET',
            url: 'editday/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#dayCode').val(s.day_code);
            $('#dayName').val(s.day_name);
            $('#dayModal').modal({backdrop: 'static', keyboard: false})
            }).fail(function (xhr, error) {

        bootbox.alert(xhr.responseText)
        });
    });

}

function clearData(){

      $('#dayCode').val('');
      $('#day-form')[0].reset();
}
function getDays() {

     $.ajax({
        type: 'GET',
        url: 'getdays',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#dayTable').DataTable().destroy();
       $("#dayTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#dayTable tbody").append(
                    "<tr>"
                    + "<td>" + item.day_name + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-day" name="id" value=' + item.day_code + '></form><button class="btn btn-outline-primary btn-sm btn-editDay" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-day" name="id" value=' + item.day_code + '></form><button class="btn btn-outline-danger btn-sm btn-deleteDay" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#dayTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}