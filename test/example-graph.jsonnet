local seed = std.extVar("seed");
local copy = std.extVar("copy");
{
    seed: seed,
    copy: {
	func: "cp_fun",
	inputs: "seed",
	args: copy,
    },
    getsrc: {
	func: "sel_key",
	inputs: 'copy',
	args: 'src',
    },
    getdst: {
	func: "sel_key",
	inputs: 'copy',
	args: 'dst',
    },
    tarsrc: {
	func: "tar_fun",
	inputs: 'getsrc',
    },
    tardst: {
	func: "tar_fun",
	inputs: 'getdst',
    },
    ls: {
	func: "ls_fun",
	inputs: ['tarsrc','tardst'],
    },
}
 
