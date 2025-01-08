function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ 'noteId': noteId })
    }).then(_ => {
        window.location.href = '/'      //refresh the page
    })
}