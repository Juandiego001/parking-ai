<template>
    <v-navigation-drawer v-model="drawer" class="bg-blue-darken-4" location="left">
        <v-list-item>
            <v-list-item-title>
                <NuxtLink to="/" class="text-white text-decoration-none">Parking AI</NuxtLink>
            </v-list-item-title>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item link to="/towers" title="Towers" prepend-icon="mdi-office-building"></v-list-item>
        <v-list-item link to="/apartments" title="Apartments" prepend-icon="mdi-home"></v-list-item>
        <v-list-item link to="/vehicles" title="Vehicles" prepend-icon="mdi-car-estate"></v-list-item>
        <v-list-item link to="/entries" title="Entries" prepend-icon="mdi-parking"></v-list-item>
    </v-navigation-drawer>

    <v-app-bar color="blue-darken-4">
        <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title>Parking AI</v-toolbar-title>
        <v-spacer></v-spacer>
        <template v-if="$vuetify.display.mdAndUp">
            <v-btn icon="mdi-plus" variant="icon" @click="createDialog=!createDialog"></v-btn>
            <v-btn icon="mdi-magnify" variant="icon" @click="searchDialog=!searchDialog"></v-btn>
        </template>

        <v-btn icon="mdi-dots-vertical" variant="text"></v-btn>
    </v-app-bar>
</template>

<script>
import { toRefs } from 'vue'
import { search } from '~/mixins/search'
import { create } from '~/mixins/create'

export default {
    setup () {
        return {
            ...toRefs(search),
            ...toRefs(create)
        }
    },
    data: () => ({
        drawer: true
    }),
    methods: {
        toggleSearchDialog () {
            console.log('LLEGA AQUI!')
            search.toggle();
        }
    }
}
</script>