const serverAddress = 'localhost:8000'

const apiCat = (api: string) =>{
    return `http://${serverAddress}${api}`
}

export default apiCat;
