{
    hello: {
	func: "echo",
	params: {
	    foo: "bar",
	    message: "{{seed.ident}} {{foo}}"
	},
	inputs: ["seed"],
    },
    final: {
	value: "hello"
    }
}
