import {api} from './api'

export const getAllItems = async () =>{
    try{
        const response = await api.get("/items")
        return response.data
    }catch(err){
        console.error(err)
        return []
    }
}

export const getItem = async (id) =>{
    try{
        const response = await api.get(`/items/${id}`)
        return response.data
    } catch(err){
        console.error(err)
        return null        
    }
}

export const addItem = async (item) =>{
    try {
        const response = await api.post("/items", item)
        return response.data

    } catch (err){
        console.error(err)
        return null
    }
}

export const updateItem = async (id, item) =>{
    try{
        const response = await api.patch(`/items/${id}`, item)
        return response.data
    }
    catch(err){
        console.error(err)
        return null
    }
}

export const deleteItem = async (id) =>{
    try{
        const response =await api.delete(`/items/${id}`)
        return response.data
    } catch (err){
        console.error(err)
        return null
    }
}