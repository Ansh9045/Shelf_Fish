import axios from 'axios'
import { getToken } from './tokenStorage'

export const api = axios.create({
    baseURL: 'http://10.235.134.83:8000',
    timeout: 900000
})

let onUnauthorized = null
export const setUnauthorizedHandler = (fn) =>{
    onUnauthorized = fn
}

api.interceptors.request.use(async (config)=>{
    const token = await getToken()
    if (token){
        config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
})

api.interceptors.response.use(
    (response) => response,
    (error) => {
        const hadToken = !!error.config?.headers?.Authorization
        if (error.response?.status === 401 && hadToken) onUnauthorized?.()
        return Promise.reject(error)
    }

)