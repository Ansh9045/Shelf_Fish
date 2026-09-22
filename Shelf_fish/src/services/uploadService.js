import axios from 'axios';
import { api } from './api';



const uploadImage = async (uri,) => {
    const formData = new FormData();
    formData.append('file', {uri, name:'photo.jpg',type: 'image/jpeg'})
    
    const response = await api.post('/detections/', formData, {headers:{
        'Content-Type':'multipart/form-data',
    }})
    return response.data
}
export {uploadImage}