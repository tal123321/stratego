function hashPassword(password) {
			return CryptoJS.SHA256(password).toString();
}

let semetricKey;
async function exchangeKeys() {
    // Generate RSA key pair
    const { publicKey, privateKey } = await window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([0x01, 0x00, 0x01]),
            hash: { name: "SHA-256" }
        },
        true,
        ["encrypt", "decrypt"]
    );

	semetricKey =generateSymmetricKey();
    // Send the public key to the server
    callServer("sendSemetricKey", semetricKey, async function(response) {
        // Convert the response bytes to a Uint8Array
        //console.log(decryptData(semetricKey,response).then(result => {
		//	console.log(result); 
		//}));
    });
}

function generateSymmetricKey() {
    // Create an array to hold the random bytes
    let keyBytes = new Uint8Array(16); // 16 bytes = 128 bits for AES-128

    // Fill the array with random values
    window.crypto.getRandomValues(keyBytes);

    // Convert the bytes to a base64-encoded string
    let keyString = btoa(String.fromCharCode.apply(null, keyBytes));

    return keyString;
}


async function encryptData(data, symmetricKeyString) {
    const pad = s => s + String.fromCharCode(16 - s.length % 16).repeat(16 - s.length % 16);
    const symmetricKey = await window.crypto.subtle.importKey(
        "raw",
        Uint8Array.from(atob(symmetricKeyString), c => c.charCodeAt(0)),
        { name: "AES-CBC" },
        false,
        ["encrypt"]
    );
    const iv = window.crypto.getRandomValues(new Uint8Array(16)); // Initialization vector for AES
    const encodedData = new TextEncoder().encode(pad(data));

    // Encrypt the data using AES-CBC algorithm
    const encryptedData = await window.crypto.subtle.encrypt(
        {
            name: "AES-CBC",
            iv: iv,
        },
        symmetricKey,
        encodedData
    );

    // Convert IV and encrypted data to base64
    const ivBase64 = btoa(String.fromCharCode.apply(null, iv));
    const encryptedDataBase64 = btoa(String.fromCharCode.apply(null, new Uint8Array(encryptedData)));

    return ivBase64 + ':' + encryptedDataBase64; // Separate IV and encrypted data with a colon
}

async function decryptData(symmetricKeyString, encryptedData) {
    // Decode the base64-encoded symmetric key string to bytes
    const keyBytes = Uint8Array.from(atob(symmetricKeyString), c => c.charCodeAt(0));

    // Import the symmetric key
    const symmetricKey = await window.crypto.subtle.importKey(
        "raw", 
        keyBytes,
        { name: "AES-CBC" },
        false,
        ["decrypt"]
    );

    // Extract IV and encrypted data from the combined string
    const ivBase64 = encryptedData.slice(0, 24); // IV is 16 bytes, base64-encoded
    const encryptedDataBase64 = encryptedData.slice(24); // Encrypted data

    // Convert IV and encrypted data to bytes
    const iv = Uint8Array.from(atob(ivBase64), c => c.charCodeAt(0));
    const encryptedBytes = Uint8Array.from(atob(encryptedDataBase64), c => c.charCodeAt(0));

    // Decrypt the data using AES-CBC algorithm
    const decryptedBytes = await window.crypto.subtle.decrypt(
        {
            name: "AES-CBC",
            iv: iv
        },
        symmetricKey,
        encryptedBytes
    );

    // Convert the decrypted bytes to string
    const decryptedData = new TextDecoder().decode(decryptedBytes);

    return decryptedData;
}
	