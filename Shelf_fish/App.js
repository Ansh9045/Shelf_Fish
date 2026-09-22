import "./global.css"
import { Text, View, ActivityIndicator } from "react-native";
import CameraComponent from "./src/components/CameraComponent";
import UploadComponent from "./src/components/UploadComponent";
import Login from "./src/pages/Login";
import { AuthProvider, useAuth } from "./src/contexts/AuthContext";
import Home from "./src/pages/Home";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Register from "./src/pages/Register"

const Stack = createNativeStackNavigator()


const AppComponent = () => {
  const { isSignedIn, loading } = useAuth()

  if (loading) {
    return <View className="flex-1 items-center justify-center">
      <ActivityIndicator size="large" color="red" />
    </View>
  }
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {isSignedIn ? (
          <>
            <Stack.Screen name="Home" component={Home} options={{ headerShown: false }} />
            <Stack.Screen name="Camera" component={CameraComponent} options={{ headerShown: false }} />
            <Stack.Screen name="Upload" component={UploadComponent} options={{ headerShown: false }} />
          </>
        ) : (
          <>
            <Stack.Screen name="Login" component={Login} options={{ headerShown: false }} />
            <Stack.Screen name="Register" component={Register} options={{ headerShown: false }} />

          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  )

}

export default function App() {

  return (
    <AuthProvider>
      <AppComponent />
    </AuthProvider>
  );
}