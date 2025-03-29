<template>
  <v-data-table :items="items" :headers="headers" :items-per-page="perPage" @update:itemsPerPage="v => perPage = v">
    <template v-slot:item.options="{ item }">
      <v-btn color="blue-darken-4" variant="icon" icon="mdi-pencil" @click="setUpdate(item.id)"></v-btn>
      <v-btn color="red-darken-4" variant="icon" icon="mdi-trash-can" @click="form = item; deleteDialog = true"></v-btn>
    </template>

    <template v-slot:item.isOwner="{ item }">
      <span>{{  item.isOwner ? 'Yes' : 'No'  }}</span>
    </template>
  </v-data-table>

  <!-- Entry Dialog -->
  <v-dialog v-model="entryDialog" max-width="500" persistent>
    <v-card>
      <v-card-title class="bg-blue-darken-4">
        <v-row no-gutters align="center">
          Create Entry
          <v-spacer></v-spacer>
          <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="isActive = false; entryDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createEntry">
          <v-row>
            <v-col cols="6">
              <v-select v-model="form.apartmentId" :items="apartments" item-title="unit" item-value="id"
                color="blue-darken-4" label="Apartment" hide-details="auto"></v-select>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.plate" color="blue-darken-4" label="Plate" hide-details="auto"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" color="blue-darken-4" label="Description"
                hide-details="auto"></v-text-field>
            </v-col>
            <v-col cols="12" class="text-end">
              <v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
              <v-btn class="mx-1" color="blue-darken-4" variant="outlined" @click="entryDialog = false; createDialog = true;">Back</v-btn>
              <v-btn type="submit" class="bg-blue-darken-4">Create</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>


  <!-- Update Dialog -->
  <v-dialog v-model="updateDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-blue-darken-4">
        <v-row no-gutters align="center">
          Update Entry
          <v-spacer></v-spacer>
          <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="updateDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="updateEntry">
          <v-row>
            <v-col cols="6">
              <v-select v-model="form.apartmentId" :items="apartments" item-title="unit" item-value="id"
                color="blue-darken-4" label="Apartment" hide-details="auto"></v-select>
            </v-col>
            <v-col cols="6">
              <v-text-field v-model="form.plate" color="blue-darken-4" label="Plate" hide-details="auto"></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field v-model="form.description" color="blue-darken-4" label="Description"
                hide-details="auto"></v-text-field>
            </v-col>
            <v-col cols="12" class="text-end">
              <v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-blue-darken-4">Update</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Create Dialog -->
  <v-dialog v-model="createDialog" max-width="600" persistent>
    <v-card>
      <v-card-title class="bg-blue-darken-4">
        <v-row no-gutters align="center">
          Init Entry
          <v-spacer></v-spacer>
          <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="isActive = false; createDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-row class="pa-5">
          <v-col class="pa-0 mb-3" cols="12">
            <video ref="video" class="w-100" poster="/public/camera-enhance-outline.svg"></video>
            <canvas ref="canvas" class="d-none"></canvas>
          </v-col>

          <v-col class="text-center" cols="12">
            <v-row class="justify-center ga-4">
              <v-btn v-if="!camActive" class="bg-blue-darken-4" @click="openCam">OPEN CAMERA</v-btn>
              <v-btn v-if="camActive" class="bg-blue-darken-4" @click="closeCam">CLOSE CAMERA</v-btn>
              <v-btn v-if="camActive && !photo" variant="outlined" color="blue-darken-4" @click="takePicture">TAKE
                PICTURE</v-btn>
              <v-btn v-if="photo" variant="outlined" color="blue-darken-4" @click="takeAnotherPicture">TAKE ANOTHER
                PICTURE</v-btn>
              <v-btn v-if="photo" color="light-blue-darken-4" @click="validatePhoto">VALIDATE ENTRY</v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Delete Dialog -->
  <v-dialog v-model="deleteDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-red-darken-4">
        <v-row no-gutters align="center">
          Delete Entry
          <v-spacer></v-spacer>
          <v-btn class="bg-red-darken-4" variant="icon" icon="mdi-close" @click="deleteDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="deleteEntry">
          <v-row>
            <v-col cols="12">
              Are you sure you want to delete the Vehicle {{ form.plate }}?
            </v-col>
            <v-col class="text-end">
              <v-btn color="red-darken-4" variant="outlined" @click="deleteDialog = false">Cancel</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-red-darken-4">Delete</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>

  <!-- Search Dialog -->
  <v-dialog v-model="searchDialog" max-width="500">
    <v-card>
      <v-card-title class="bg-blue-darken-4">
        <v-row no-gutters align="center">
          Search Entry
          <v-spacer></v-spacer>
          <v-btn class="bg-blue-darken-4" variant="icon" icon="mdi-close" @click="searchDialog = false"></v-btn>
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="search" label="Plate"></v-text-field>
            </v-col>

            <v-col class="text-end" cols="12">
              <v-btn color="blue-darken-4" variant="outlined" @click="updateDialog = false">Cancel</v-btn>
              <span class="mx-1"></span>
              <v-btn type="submit" class="bg-blue-darken-4">Search</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { toRefs } from 'vue'
import { search } from '~/mixins/search'
import { create } from '~/mixins/create'

definePageMeta({
  layout: 'app'
})

export default {
  setup() {
    return {
      ...toRefs(search),
      ...toRefs(create)
    }
  },
  data: () => ({
    apartments: [],
    items: [],
    search: '',
    page: 1,
    perPage: 15,
    form: {
      id: '',
      plate: '',
      isOwner: '',
      description: '',
      apartmentId: '',
      status: '',
      created_at: '',
      updated_at: ''
    },
    entryDialog: false,
    updateDialog: false,
    deleteDialog: false,
    camActive: false,
    media: '',
    photo: '',
    isActive: true,
  }),
  computed: {
    headers() {
      return [
        { title: 'Id', key: 'id' },
        { title: 'Plate', key: 'plate' },
        { title: 'Apartment', key: 'apartmentId' },
        { title: 'Owner', key: 'isOwner' },
        { title: 'Options', key: 'options', align: 'center' }
      ]
    }
  },
  watch: {
    async createDialog(val) {
      if (!val && !this.isActive) this.closeCam();
    },
    async entryDialog (val) {
      if (!val && !this.isActive) this.closeCam();
      else await this.getApartments();
    }
  },
  async beforeMount() {
    await this.getEntries()
  },
  methods: {
    async getApartments() {
      try {
        const { items } = await $fetch('/api/apartments/', { method: 'GET' })
        this.apartments = items
      } catch (err) {
        console.log(err)
      }
    },
    async getEntries() {
      try {
        const { items } = await $fetch('/api/entries/', {
          method: 'GET',
          query: {
            search: this.search,
            page: this.page,
            perPage: this.perPage
          }
        })
        this.items = items
      } catch (err) {
        console.log(err)
      }
    },
    async createEntry() {
      try {
        const { message } = await $fetch('/api/entries/', {
          method: 'POST',
          body: this.form
        })
        console.log('RESPONSE: ', message);
        await this.getEntries();
        this.entryDialog = false;
        this.isActive = false;
      } catch (err) {
        console.log(err);
      }
    },
    async setUpdate(entryId) {
      try {
        this.form = await $fetch(`/api/entries/${entryId}`, {
          method: 'GET'
        })
        this.updateDialog = true
      } catch (err) {
        console.log(err);
      }
    },
    async updateEntry() {
      try {
        const response = await $fetch(`/api/entries/${this.form.id}`, {
          method: 'PUT',
          body: this.form
        })
        console.log('RESPONSE UPDATE: ');
        console.log(response);
        await this.getEntries()
        this.updateDialog = false;
      } catch (err) {
        console.log(err);
      }
    },
    async deleteEntry() {
      try {
        const response = await $fetch(`/api/entries/${this.form.id}`, { method: 'DELETE' })
        console.log('RESPONSE DELETE: ');
        console.log(response);
        await this.getEntries()
        this.deleteDialog = false
      } catch (err) {
        console.log(err)
      }
    },
    async doSearch() {
      await this.getEntries();
      this.searchDialog = false;
    },
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
        if (this.$refs.video) this.$refs.video.src = '';
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

        const width = this.$refs.video.getBoundingClientRect().width;
        const height = this.$refs.video.getBoundingClientRect().height;

        this.$refs.canvas.width = width;
        this.$refs.canvas.height = height;


        context.drawImage(this.$refs.video, 0, 0, this.$refs.canvas.width, this.$refs.canvas.height);
        this.photo = this.$refs.canvas.toDataURL('image/png');
      } catch (err) {
        console.log(err);
      }
    },
    async takeAnotherPicture() {
      try {
        this.$refs.video.play();
        this.photo = ''
      } catch (err) {
        console.log(err);
      }
    },
    async validatePhoto() {
      try {
        const { message, isOwner, plate } = await $fetch('/api/entries/validate/photo', {
          method: 'POST',
          body: {
            photo: this.photo
          }
        });

        this.isActive = true;
        this.form = {
          isOwner,
          plate
        };

        this.$nextTick(() => {
          this.createDialog = false;
          this.entryDialog = true;
        })
      } catch (err) {
        console.log(err);
      }

    }
  }
}
</script>