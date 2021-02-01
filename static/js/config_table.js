var $modal_delete = $('#modal_delete')
var $table = $('#table')
var $btn_delete = $("#btn_delete")



$(document).ready(function () {
    selections = getIdSelections()
    if (selections <= 0) {
        $modal_delete.prop('disabled', true)
    }
})

$modal_delete.click(function () {
    $("#preview_delete > tbody").empty()
    var entries_id = getIdSelections()
    var entries_name = getNameSelections()
    for (i = 0; i < entries_id.length; i++) {
        $("#preview_delete > tbody").append(`<tr><td>${entries_id[i]}</td><td>${entries_name[i]}</td></tr>`)
    }
})

$btn_delete.click(function () {
    var entries = getIdSelections()
    $modal_delete.prop('disabled', true)
    delete_entries(entries)
    $('.modal').modal('hide')
})

$("#table").bootstrapTable({
    exportOptions: {
        ignoreColumn: [-1, -2]
    }
})

function stateFormatter(value, row, index) {
    if (row.uuid in ["1", "0"]) {
        return {
            disabled: true,
            checked: false
        }
    }
}

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.uuid
    })
}

function getNameSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.name
    })
}

function getSubjectSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.subject
    })
}

$("#table").on('check.bs.table uncheck.bs.table ' +
    'check-all.bs.table uncheck-all.bs.table',
    function () {
        selections = getIdSelections()
        $modal_delete.prop('disabled', !$table.bootstrapTable('getSelections').length)
        console.log(selections)
    })

