<template>
    <v-data-table :items="items"></v-data-table>
</template>

<script>

definePageMeta({
    layout: 'app'
})

export default {
    data: () => ({
        items: [
            {
                plate: 'RUB892',
                options: '',
            },
        ]
    })
}
</script>
