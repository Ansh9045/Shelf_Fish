import { StyleSheet, Text, View, Button, TouchableOpacity } from 'react-native'
import {useState} from 'react'
import { CameraView, CameraType, useCameraPermissions } from 'expo-camera'

const CameraComponent = () => {
    const [facing, setFacing] = useState('back')
    const [permissions, requestPermissions] = useCameraPermissions();

    if (!permissions){
        return <View/>
    }
    if (!permissions.granted){
        return(
            <View className="flex-1 items-center justify-center">
                <Text className="text-xl">We need your permission to show the camera</Text>
                <Button onPress={requestPermissions} title="Grant Permission" />
            </View>
        )
    }

    const toggleCamera = ()=>{
        setFacing(current => (current == "back" ? "front" : "back"))
    }
    
  return (
    <View className="flex-1 justify-center" >
        <CameraView style={{flex:1}} facing={facing}/>
        <View className="absolute bottom-40 flex-row bg-transparent w-full px-3">
            <TouchableOpacity className="flex-1 items-center" onPress={toggleCamera}>
                <Text>Flip Camera</Text>
            </TouchableOpacity>
        </View>
    </View>
  )
}

export default CameraComponent

const styles = StyleSheet.create({})