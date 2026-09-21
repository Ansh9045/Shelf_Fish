import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native'
import { useState, useRef } from 'react'
import { CameraView, useCameraPermissions } from 'expo-camera'
import { uploadImage } from '../services/uploadService'


const CameraComponent = () => {
    const [facing, setFacing] = useState('back')
    const [permissions, requestPermissions] = useCameraPermissions();
    const [uploading, setUploading] = useState(false)
    const cameraRef = useRef(null)


    if (!permissions) {
        return <View />
    }
    if (!permissions.granted) {
        return (
            <View className="flex-1 items-center justify-center">
                <Text className="text-xl">We need your permission to show the camera</Text>
                <Button onPress={requestPermissions} title="Grant Permission" />
            </View>
        )
    }

    const toggleCamera = () => {
        setFacing(current => (current == "back" ? "front" : "back"))
    }

    const capture = async ()=>{
        if (!cameraRef.current || uploading) return
        try{
            setUploading(true)
            const photo = await cameraRef.current.takePictureAsync({quality: 0.7})
            const r = await uploadImage(photo.uri)
            console.log(r)
        } catch(e){
            console.error(`Error Uploading Image ${e}`)
        }
        finally{
            setUploading(false)
        }
    }

    return (
        <View className="flex-1 justify-center" >
            <CameraView style={{ flex: 1 }} facing={facing} ref={cameraRef}/>
            <View className="absolute bottom-40 flex-row bg-transparent w-full px-3">
                <TouchableOpacity className="flex-1 items-center" onPress={toggleCamera}>
                    <Text>Flip Camera</Text>
                </TouchableOpacity>
                <TouchableOpacity className="flex-1 items-center" onPress={capture}>
                    <Text>{uploading ? "Uploading...": "Capture"}</Text>
                </TouchableOpacity>

            </View>
        </View>
    )
}

export default CameraComponent

const styles = StyleSheet.create({})