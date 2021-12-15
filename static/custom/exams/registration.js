

$(document).ready(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
            }
        });
formatDate()
searchType();
searchGrading();
searchYear();
gradingChange();
yearChange();
typeChange();
searchTerm();
termChange();
monthChange();
saveExamRegister();
getExamRegister();
editExam();
clickClear();
deleteRegistration();
});
function clickClear() {
  $('#newRegister').click(function () {
      clearData()
  })
}
function formatDate() {
    var d = new Date()
        var n = new Date()
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();
    var newDate = new Date(n.setMonth(n.getMonth()+1));
     month2 = ''+ (newDate.getMonth() + 1);
     day2 = '' + newDate.getDate();
     year2 = newDate.getFullYear();
    // var jan312009 = new Date(2009, 0, 31);
    // var eightMonthsFromJan312009  = jan312009.setMonth(jan312009.getMonth()+8);
 console.log(newDate)
    console.log(month2)
    console.log(year2)
    console.log(day2)
    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;


    if (month2.length < 2)
        month2 = '0' + month2;
    if (day2.length < 2)
        day2 = '0' + day2;

    // var month2=d.getMonth()+2;


    $('#effectiveDate').val([year, month, day].join('-'));
    $('#lockDate').val([year2, month2, day2].join('-'));

}
function searchType() {
        $('#type_frm').select2({
            placeholder: 'Exam Type',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamtype',
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
function getExamRegister() {
     $.ajax({
        type: 'GET',
        url: 'getexamreg',
        processData: false,
        contentType: false,
    }).done(function (s) {
         $('#examTable').DataTable().destroy();
        $("#examTable tbody").empty();
        $.each(s,function(i,item){
            $("#examTable tbody").append(
                "<tr>"
                +"<td>"+item.examName+"</td>"
                +"<td>"+item.yearNumber+"</td>"
                +"<td>"+item.month+"</td>"
                +"<td>"+item.typeName+"</td>"
                +"<td>"+item.termNumber+"</td>"
                +"<td>"+item.finalExam+"</td>"
                +"<td>"+item.status+"</td>"
                +"<td>"+item.national+"</td>"
                +"<td>"+item.gradingName+"</td>"
                +"<td>"+item.effectiveDate+"</td>"
                +"<td>"+item.lockDate+"</td>"
                +"<td>"+'<form id="editForm" method="post" enctype="multipart/form-data"><input type="hidden" id="edit-exam" name="id" value='+item.regCode+'></form><button class="btn btn-outline-primary btn-sm btn-editexam" ><i class="fa fa-edit"></button>'
                +"</td>"
                +"<td>"+'<form id="deleteForm" method="post" enctype="multipart/form-data"><input type="hidden" id="delete-exam" name="id" value='+item.regCode+'></form><button class="btn btn-outline-danger btn-sm btn-deleteexam" ><i class="fa fa-trash-o"></button>'
                +"</tr>" )
        })
        $('#examTable').DataTable();
    }).fail(function (xhr, error) {
       bootbox.alert(xhr.responseText);
    });

}
function searchTerm() {
        $('#term_frm').select2({
            placeholder: 'Term',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamterm',
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
function searchGrading() {
        $('#grading_frm').select2({
            placeholder: 'Grading',
            allowClear: true,
                        width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamgrading',
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
function editExam(){
    $('#examTable').on('click','.btn-editexam',function (s) {
        var data=$(this).closest('tr').find('#edit-exam').val();
        $.ajax({
            type: 'GET',
            url: 'editexamreg/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
            $('#regCode').val(s.regCode);
            $('#month').val(s.month);
            $('#effectiveDate').val(s.effectiveDate);
            $('#lockDate').val(s.lockDate);
            $('#displayName').val(s.displayName);
            $('#examName').val(s.examName);
            $('#termName').val('T'+s.termNumber+'_')
            $('#monthName').val('_'+s.month)
            $('#yearName').val('_'+s.yearNumber)
            $('#typeName').val('_'+s.typeName)


            if (s.finalExam === true) {
                $('#finalExam').prop('checked', true);
            }
            else {
                $('#finalExam').prop('checked', false);

            }
               if (s.combinedExam === true) {
                $('#combinedExam').prop('checked', true);
            }
            else {
                $('#combinedExam').prop('checked', false);

            }

            if (s.gradeCode) {
                $('#gradeCode').val(s.gradeCode)
                var $newCode = $("<option selected='selected' value='" + s.gradeCode + "'>'+s.gradeName+'</option>").val(s.gradeCode.toString()).text(s.gradeName)
                $('#grading_frm').append($newCode).trigger('change');
            }
            else {
                $('#gradeCode').val('')
                $('#grading_frm').empty();
            }
             if (s.yearCode) {
                $('#yearCode').val(s.yearCode)
                var $newYear = $("<option selected='selected' value='" + s.yearCode + "'>'+s.yearNumber+'</option>").val(s.yearCode.toString()).text(s.yearNumber)
                $('#year_frm').append($newYear).trigger('change');
            }
            else {
                $('#yearCode').val('')
                $('#year_frm').empty();
            }
             if (s.typeCode) {
                $('#typeCode').val(s.typeCode)
                var $newType = $("<option selected='selected' value='" + s.typeCode + "'>'+s.typeName+'</option>").val(s.typeCode.toString()).text(s.typeName)
                $('#type_frm').append($newType).trigger('change');
            }
            else {
                $('#typeCode').val('')
                $('#type_frm').empty();
            }
             if (s.termCode) {
                $('#termCode').val(s.termCode)
                var $newTerm = $("<option selected='selected' value='" + s.termCode + "'>'+s.termNumber+'</option>").val(s.termCode.toString()).text(s.termNumber)
                $('#term_frm').append($newTerm).trigger('change');
            }
            else {
                $('#termCode').val('')
                $('#term_frm').empty();
            }

        }).fail(function (xhr, error) {
        bootbox.alert(xhr.responseText)
        });
    });

}
function clearData() {
    $('#reg-form')[0].reset();
    $('#type_frm').empty();
    $('#year_frm').empty();
    $('#grading_frm').empty();
    $('#term_frm').empty();
    $('#regCode').val('');
    $('#typeCode').val('');
    $('#typeName').val('');
    $('#yearCode').val('');
    $('#yearName').val('');
    $('#gradeCode').val('');
    $('#termCode').val('');
    $('#termName').val('');
    formatDate()
}
function saveExamRegister(){
     $('#saveRegister').click(function () {
        var data=$('#reg-form').serialize();
        var url = '';
        if($('#regCode').val()===''){
          url = 'createregister'
        }else{
            url = 'updateregister/'+$('#regCode').val()
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
		    getExamRegister()
            clearData()


		}).fail(function (xhr, error) {
						bootbox.alert(xhr.responseText)
            // bootbox.alert("Error Occured while saving")
		})


	})
}
function deleteRegistration() {
     $('#examTable').on('click','.btn-deleteexam',function (s) {
        var data = $(this).closest('tr').find('#delete-exam').val();
        bootbox.confirm("Are you sure want to delete this Exam?", function (result) {
            if (result) {
               $.ajax({
            type: 'GET',
            url: 'deleteexam/'+data,
            processData: false,
            contentType: false,
        }).done(function (s) {
          getExamRegister()
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
function searchYear() {
        $('#year_frm').select2({
            placeholder: 'Year',
            allowClear: true,
            width: '67%',
            ajax: {
                delay: 250,
                url: 'searchexamyear',
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
function monthChange(){
   
    $('#month').change(function () {

       $('#monthName').val('_'+$('#month').val())
        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())

    })

    
}
function typeChange() {
    $('#type_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#typeCode').val(data.id);
        $('#typeName').val('_'+data.text);
        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())

    });
    $("#type_frm").on("select2:unselecting", function(e) {
    $('#typeName').val('');
    $('#typeCode').val('')
 });
}
function yearChange() {
    $('#year_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#yearCode').val(data.id)
        $('#yearName').val('_'+data.text)

        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())

    });
    $("#year_frm").on("select2:unselecting", function(e) {
    $('#yearCode').val('')
    $('#yearName').val('')

 });
}
function gradingChange() {
    $('#grading_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#gradeCode').val(data.id)
        $('#gradeName').val(data.text)
        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())

    });
    $("#grading_frm").on("select2:unselecting", function(e) {
    $('#gradeCode').val('')
    $('#gradeName').val('')

 });
}
function termChange() {
    $('#term_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#termCode').val(data.id)
         $('#termName').val('T'+data.text+'_')
        $('#examName').val($('#termName').val()+$('#monthName').val()+$('#yearName').val()+$('#typeName').val())

    });
    $("#term_frm").on("select2:unselecting", function(e) {
    $('#termCode').val('')
    $('#termName').val('')

 });
}