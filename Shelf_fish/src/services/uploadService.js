import axios from 'axios';
const api = axios.create({
    baseURL: 'http://10.55.131.83:8000',
    timeout: 900000
})

const uploadImage = async (uri) => {
    const formData = new FormData();
    formData.append('file', {uri, name:'photo.jpg',type: 'image/jpeg'})
    
    const response = await api.post('/detections/', formData, {headers:{
        'Content-Type':'multipart/form-data',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc4OTk4NTgxNn0.k17WU2LGSFj4uHNiJvgYdxUxqFO1n7cxuBMDIRYyGHM'
    }})
    return response.data
}
export {uploadImage}