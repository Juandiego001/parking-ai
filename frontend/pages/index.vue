<template>
    <v-container class="fill-height justify-center" fluid>
        <v-row class="justify-center">
            <v-col>
                <NuxtLink class="text-decoration-none" to="/towers">
                    <v-card class="mx-auto" width="300">
                        <v-card-text class="pa-0">
                            <v-img width="300" height="200" src="/buildings.jpg" cover></v-img>
                        </v-card-text>
                        <v-card-actions class="bg-blue-darken-4 justify-center">
                            <v-icon icon="mdi-office-building"></v-icon>
                            <p>Towers</p>
                        </v-card-actions>
                    </v-card>
                </NuxtLink>
            </v-col>

            <v-col>
                <NuxtLink class="text-decoration-none" to="/apartments">
                    <v-card class="mx-auto" width="300">
                        <v-card-text class="pa-0">
                            <v-img width="300" height="200" src="/apartment.jpg" cover></v-img>
                        </v-card-text>
                        <v-card-actions class="bg-blue-darken-4 justify-center">
                            <v-icon icon="mdi-home"></v-icon>
                            <p>Aparments</p>
                        </v-card-actions>
                    </v-card>
                </NuxtLink>
            </v-col>

            <v-col>
                <NuxtLink class="text-decoration-none" to="/vehicles">
                    <v-card class="mx-auto" width="300">
                        <v-card-text class="pa-0">
                            <v-img width="300" height="200" src="/cars.jpg" cover></v-img>
                        </v-card-text>
                        <v-card-actions class="bg-blue-darken-4 justify-center">
                            <v-icon icon="mdi-car-estate"></v-icon>
                            <p>Vehicles</p>
                        </v-card-actions>
                    </v-card>
                </NuxtLink>
            </v-col>

            <v-col>
                <NuxtLink class="text-decoration-none" to="/entries">
                    <v-card class="mx-auto" width="300">
                        <v-card-text class="pa-0">
                            <v-img width="300" height="200" src="/gatehouse.jpg" cover></v-img>
                        </v-card-text>
                        <v-card-actions class="bg-blue-darken-4 justify-center">
                            <v-icon icon="mdi-parking"></v-icon>
                            <p>Entries</p>
                        </v-card-actions>
                    </v-card>
                </NuxtLink>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

definePageMeta({
    layout: 'app'
})

export default {
    data: () => ({
        entryDialog: false,
        camActive: false,
        media: '',
        photo: ''
    }),
    watch: {
        entryDialog (val) {
            if (!val) this.closeCam();
        }
    },
    methods: {
        async openCam() {
            try {
                const constraints = {
                    video: { width: 1280, height: 720 },
                };

                this.media = await navigator.mediaDevices.getUserMedia(constraints);
                this.$refs.video.srcObject = this.media;
                this.$refs.video.onloadedmetadata = () => this.$refs.video.play();
                this.camActive = true;
            } catch (err) {
                console.log(err);
            }
        },
        async closeCam() {
            try {
                this.$refs.video.src = '';
                const videoTrack = this.media.getVideoTracks()[0];
                videoTrack.stop();
                this.media.removeTrack(videoTrack);
                this.camActive = false;
                this.photo = ''
            } catch (err) {
                console.log(err);
            }
        },
        async takePicture() {
            try {
                this.$refs.video.pause();
                const context = this.$refs.canvas.getContext('2d');
                context.drawImage(this.$refs.video, 0, 0, this.$refs.video.width, this.$refs.video.height);
                this.photo = this.$refs.canvas.toDataURL('image/png');
            } catch (err) {
                console.log(err);
            }
        },
        async takeAnotherPicture () {
            try {
                this.$refs.video.play();
                this.photo = ''
            } catch (err) {
                console.log(err);
            }
        },
        async validatePhoto () {
            try {
                console.log('LLEGA A VALIDAR PHOTO');
                const formData = new FormData();
                formData.append('photo', this.photo);
                const response = $fetch('/api/entries/', {
                    method: 'POST',
                    body: formData
                });
                console.log('RESPONSE: ', formData);
            } catch (err) {
                console.log(err);
            }

        }
    }
}
</script>
