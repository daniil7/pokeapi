window.PAGINATION_COUNT = 0;

export default class Pagination 
{
    constructor(one_page_limit)
    {
        this.current_page = 0;
        this.one_page_limit = one_page_limit;
        this.pages_count = 0;
    }

    paginate(data) {
        this.pages_count = Math.ceil(
            data.length / this.one_page_limit
        );
        if (this.current_page >= this.pages_count)
            this.current_page = 0;
        let paginated = data.slice(
            this.current_page * this.one_page_limit,
            (this.current_page+1) * this.one_page_limit
        );
        return paginated;
    }

    static links(variable_name) {
        return `
        <div class="flex flex-wrap mt-4">
            <template x-for="page in ${variable_name}.pages_count">
                <div x-bind:class="'flex items-center justify-center border-solid border-2 border-indigo-600 p-2 mx-1 mb-1 min-w-[2.5rem] min-h-[2.5rem] cursor-pointer' +
                                   (${variable_name}.current_page == page-1 ? ' bg-indigo-600 text-white' : '')"
                    x-text="page"
                    x-on:click="${variable_name}.current_page = page-1"></div>
            </template>
        </div>
        `;
    }
}
