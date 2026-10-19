import {Alert,Button, StyleSheet, Text, View } from 'react-native'
import React, { useState } from 'react'
import * as ImagePicker from 'expo-image-picker'
import { uploadImage } from '../services/uploadService'
import {useNavigation} from '@react-navigation/native'

const UploadComponent = () => {
    const navigation = useNavigation()
    const pickImage = async () =>{
        const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync()
        
        if (!permissionResult.granted){
            Alert.alert('Permission Required', 'Permission to access media library is required');
            return
        }
        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ['images'],
            allowsEditing: true,
            quality: 0.5
        })

        const r = await uploadImage(result.assets[0].uri)
        navigation.navigate("ItemCreate", {item: r})
        console.log(r)

    }

    return (
        <View className="flex-1 items-center justify-center">
            <Button title={"Choose an image"} onPress={pickImage} />
        </View>
    )
}

export default UploadComponent

const styles = StyleSheet.create({})