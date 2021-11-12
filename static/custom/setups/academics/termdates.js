$(document).ready(function () {
    $.ajaxSetup({
        headers: {
            "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
        }
    });

      formatDate();
      termModal();
      saveTerm();
      getTermDates();
      searchClass();
      classChange();
      editTerm();
      deleteTerm();
})
function classChange(){
    $('#class-frm').on('select2:select', function (e) {
    var data = e.params.data;
    $('#class-id').val(data.id)
    $('#class-name').val(data.text)

});
    $("#class-frm").on("select2:unselecting", function(e) {
    $('#class-id').val('')
    $('#class-name').val('')
 });
}
function termModal() {
    $('#open-modal').click(function () {
        $('#termModal').modal({backdrop: 'static', keyboard: false})
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

    $('#fromDate').val([year, month, day].join('-'))
    $('#toDate').val([year, month, day].join('-'))

}

function saveTerm() {
    $('#saveTerm').click(function () {
        var data = $('#term-form').serialize();
        var url = '';
        if ($('#termCode').val() === '') {
            url = 'createtermdates'
        } else {
            url = 'updatetermdates/' + $('#termCode').val()
        }
        $.ajax({
            type: 'POST',
            url: url,
            data: data
        }).done(function (s) {
            getTermDates()
            clearData()
            $('#termModal').modal('hide')
            bootbox.alert(s.success)

        }).fail(function (xhr, error) {
            bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
        })


    })
}
function clearData(){
      $('#class-frm').empty();
      $('#teacher-id').val('');
      $('#class-id').val('');
      $('#term-form')[0].reset();
      $('#termCode').val('');
}
function deleteTerm() {
    $('#termTable').on('click','.btn-deleteTerm',function (s) {
        var data = $(this).closest('tr').find('#delete-term').val();
        bootbox.confirm("Are you sure want to delete this Term?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deletetermdates/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          bootbox.hideAll()
          getTermDates()
          bootbox.alert(s.success)


        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
            }
        })
    })
}

function getTermDates() {
     $.ajax({
        type: 'GET',
        url: 'gettermdates',
        processData: false,
        contentType: false,
    }).done(function (s) {
       $('#termTable').DataTable().destroy();
       $("#termTable tbody").empty();
        if(s.length!==0) {
            $.each(s, function (i, item) {
                $("#termTable tbody").append(
                    "<tr>"
                    + "<td>" + item.termNumber + "</td>"
                    + "<td>" + item.className + "</td>"
                    + "<td>" + item.fromDate + "</td>"
                    + "<td>" + item.toDate + "</td>"
                    + "<td>" + item.currentTerm + "</td>"
                    + "<td>" + '<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-term" name="id" value=' + item.termCode + '></form><button class="btn btn-outline-primary btn-sm btn-editTerm" ><i class="fa fa-edit"></button>'
                    + "</td>"
                    + "<td>" + '<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-term" name="id" value=' + item.termCode + '></form><button class="btn btn-outline-danger btn-sm btn-deleteTerm" ><i class="fa fa-trash-o"></button>'
                    + "</tr>")
            })
        }
        $('#termTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}

function editTerm(){
    $('#termTable').on('click','.btn-editTerm',function (s) {
        var data=$(this).closest('tr').find('#edit-term').val();
        $.ajax({
            type: 'GET',
            url: 'edittermdates/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#termCode').val(s.termCode);
            $('#termNumber').val(s.termNumber).change();
            $('#fromDate').val(s.fromDate);
            $('#toDate').val(s.toDate);
            if (s.currentTerm === true) {
                $('#currentTerm').prop('checked', true);
            }
            else {
                $('#currentTerm').prop('checked', false);

            }
            if (s.classCode) {
                $('#class-id').val(s.classCode)
                var $newClass = $("<option selected='selected' value='" + s.classCode + "'>'+s.className+'</option>").val(s.classCode.toString()).text(s.className)

                $('#class-frm').append($newClass).trigger('change');
            }
            else {
                $('#class-id').val('')
                $('#class-frm').empty();
            }

        $('#termModal').modal({backdrop: 'static', keyboard: false})
        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function searchClass() {
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