import { StyleSheet, KeyboardAvoidingView, Platform, Text, View, Image, Pressable, Alert, ScrollView, TextInput } from 'react-native'
import React, { useState, useEffect } from 'react'
import { addItem } from '../services/itemService'

const dummy = { "brand": "Oreo", "category": "Sandwich Cookies", "created_at": "2026-09-23T11:49:02.671240", "id": 25, "img_url": "https://res.cloudinary.com/emnvyz0h/image/upload/v1790164141/detections/m6u1ki3yiclqkkxfxfq5.jpg", "name": "Double Stuf Oreo", "tags": ["oreo", "double stuf oreo", "chocolate sandwich cookies", "creme filled cookies", "nabisco cookies"], "user_id": 2 }

const Offset = ({ color, children, className = '', size = 10 }) => {
  return (
    <View className={`relative ${className}`}>
      <View
        style={{ position: 'absolute', backgroundColor: color, transform: [{ translateX: size }, { translateY: size }], inset: 0 }}
        className={`absolute inset-0 bg-${color} translate-x-[${size}px] translate-y-[${size}px]`} />
      {children}
    </View>
  )
}

const Stripes = ({ primary, secondary, length, className = '' }) => {
  return (
    <View className={`flex-row h-3 ${className}`}>
      {Array.from({ length: length }).map((_, i) => {
        return (
          <View
            key={i}
            className={`flex-1 ${i % 2 === 0 ? `bg-${primary}` : `bg-${secondary}`}`}

          />
        )
      })}
    </View>
  )
}

const Field = ({ label, value, onChangeText, placeholder, className='' }) => {
  return (

    <View
      className={`flex w-full justify-center items-start px-6 mt-5 ${className}`}
    >
      <Text className="text-start font-black text-deep-red text-lg">{label}</Text>
      <Offset color="black" className="w-[90%]">
        <TextInput
          value={value}
          onChangeText={onChangeText}
          placeholder={placeholder}
          className="border-[6px] border-amber-400 w-full bg-deep-red text-gray-100 px-6 text-xl"
        />
      </Offset>

    </View>
  )
}

const ItemCreate = ({ route }) => {
  const item = dummy
  console.log(item)
  const [quantity, setQuantity] = useState(1)
  const [error, setError] = useState('')
  const [name, setName] = useState(item?.name ?? '')
  const [brand, setBrand] = useState(item?.brand ?? '')
  const [category, setCategory] = useState(item?.category ?? '')
  const [tags, setTags] = useState(item?.tags ?? [])
  const [tagInput, setTagInput] = useState('')
  const [addingTag, setAddingTag] = useState(false)
  const [removing, setRemoving] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  const incQuantity = () => {
    setQuantity(p => p += 1)
  }
  const decQuantity = () => {
    if (quantity > 1) {
      setQuantity(p => p -= 1)
    }
    else {
      setError('There is only one item in stock, if you want to discard it, use the discard button')
    }
  }

  const addTag = () => {
    if (addingTag) {
      const trimmed = tagInput.trim()
      if (!trimmed) {
        setError("Write something in the input field to add a tag!!!")
      }
      else if (tags.includes(trimmed)) {
        setError(`${trimmed} is alread present in tags`)
      }
      else {
        setTags(prev => [...prev, trimmed])
      }
      setTagInput('')
    }
  }
  const toggleRemoving = () => {
    setRemoving(prev => !prev)
  }
  const removeTag = (ind) => {
    if (removing) {
      setTags(prev => prev.filter((_, i) => i !== ind))
    }
  }

  const handleAdd = async () => {
    if (submitting) return
    setSubmitting(true)
    try {
      const response = await addItem({
        name,
        brand,
        category,
        img_url: item?.img_url ?? '',
        quantity,
        tags,
        price: 100
      })
    } catch (e) {

    }
    finally {

    }
  }

  useEffect(() => {
    if (error) {
      Alert.alert('Error', error, [{ text: 'OK', onPress: () => setError('') }])
    }
  }, [error])


  return (
    <KeyboardAvoidingView className="flex-1" behavior={Platform.OS === "ios" ? "padding" : "height"}>

      <ScrollView className="flex-1 bg-gray-300">
        <View className="flex flex-1 items-center justify-start gap-4 pb-6">

          <View className="bg-deep-red w-full flex mb-6 pb-24 pt-8">
            <View className="flex-row items-center justify-between px-5">
              <Text className="text-7xl text-amber-400  text-start ">ADD {'\n'}ITEM</Text>
              <Image source={require('../../assets/logo.png')} className="h-36 w-36" />
            </View>

            <View className="border-t-2 border-amber-400 mt-4 pr-8 absolute bottom-16 left-4 pt-2">
              <Text className="text-amber-400 font-bold">Ministry of the fish</Text>
            </View>


            <Text className="bg-zinc-900 absolute bottom-6 tracking-wide text-deep-red py-2 -rotate-[4deg] capitalize font-black -left-1 text-center -right-1 text-[13px] border-y-2 border-amber-400 ">★ Fulfill your duties by adding items for the STATE ★</Text>


          </View>
          <Offset color="#7a0000" className="w-[80%]" size={12}>
            <Image source={{ uri: item?.img_url }} className="w-full aspect-square border-[8px] border-amber-400" />
          </Offset>


          <Field
            label="Brand"
            value={brand}
            onChangeText={setBrand}
            placeholder="Brand"
          />

          <Field
            label="Name"
            value={name}
            onChangeText={setName}
            placeholder="Name"
          />
          <Field
            label="Category"
            value={category}
            onChangeText={setCategory}
            placeholder="Category"
          />


          <View className="flex justify-center items-start px-6 mt-8">
            <View className="flex-row items-center justify-between w-full mb-2">
              <Text className="text-start font-black text-xl text-deep-red mb-3">Tags </Text>
              <Pressable onPress={toggleRemoving}>
                {removing ? (
                  <View className="relative">
                    <View className="absolute inset-0 bg-black translate-x-[4px] translate-y-[4px]" />
                    <Text className="text-xl text-deep-red font-black px-2 py-0.5 bg-gray-300 border-2 border-deep-red">X</Text>
                  </View>) : (
                  <View className="relative">
                    <View className="absolute inset-0 bg-black translate-x-[4px] translate-y-[4px]" />
                    <Text className="text-xl text-deep-red font-black px-2 py-0.5 bg-amber-400 border-2 border-deep-red">X</Text>
                  </View>
                )}
              </Pressable>
            </View>

            <View className="flex-row flex-wrap gap-3">

              {tags.map((tag, ind) => (
                <View key={ind}>
                  <View className="absolute inset-0 bg-black translate-x-[6px] translate-y-[6px]" />
                  <Pressable onPress={() => removeTag(ind)} className={`border-4 border-deep-red bg-amber-400 flex-row items-center gap-2 ${removing ? "pl-4" : "px-4"}`}>
                    <Text className={`text-black font-black ${removing ? "text-lg" : ""}`}>{tag.toUpperCase()}</Text>
                    {removing && (
                      <View className="bg-deep-red px-3 py-1">
                        <Text className="text-white font-thin">X</Text>
                      </View>
                    )}
                  </Pressable>
                </View>
              ))}
            </View>


          </View>
          <View className="mt-4 bg-gray-300 border-1 border-black">
            <View className="bg-black absolute inset-0 translate-y-[10px] translate-x-[10px] -z-10" />
            <View className="flex-row items-center justify-center gap-4 border-4 border-amber-400">

              <Pressable onPress={decQuantity} className="bg-deep-red w-12 flex items-center justify-center aspect-square border-r-4 border-amber-400">
                <Text className="text-xl text-amber-400 font-black">-</Text>
              </Pressable>

              <Text className="text-xl text-deep-red font-black">{quantity}</Text>

              <Pressable onPress={incQuantity} className="bg-deep-red w-12 flex items-center justify-center aspect-square border-l-4 border-amber-400">
                <Text className="text-lg text-amber-400 font-black">+</Text>
              </Pressable>
            </View>

          </View>




          <Pressable onPress={handleAdd} disabled={submitting} className="mt-8">
            {({ pressed }) => (
              <View className="-rotate-[2deg]">
                <View className="absolute top-2 -bottom-2 left-2 -right-2 bg-black/80" />
                <View
                  className={`border-4 border-black bg-amber-400 ${pressed ? "translate-x-2 translate-y-2" : "translate-x-0 translate-y-0"}`}
                >
                  <View className="flex-row items-stretch">
                    <View className="bg-deep-red w-20 flex items-center justify-center border-r-4 border-black p-1">
                      <Image source={require('../../assets/logo.png')} className="w-[65px] p-1 h-[65px]" />

                    </View>
                    <View className="justify-center items-center px-4  py-3">
                      <Text className="text-3xl text-deep-red font-black tracking-wide">{submitting ? "ADDING..." : "ADD TO STATE"}</Text>
                      <Text className="text-xs font-bold tracking-wide text-black">{`Adding x${quantity} unit${quantity > 1 ? "s" : ""} for the people`}</Text>
                    </View>
                    <View className="bg-black w-16 flex items-center justify-center">
                      <Text className="text-2xl text-amber-400 font-black">►</Text>
                    </View>
                  </View>
                </View>

              </View>
            )}

          </Pressable>

        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  )
}

export default ItemCreate

const styles = StyleSheet.create({})