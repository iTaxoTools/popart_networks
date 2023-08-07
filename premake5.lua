workspace("Popart_Networks")
	configurations({"debug", "release"})

	newoption({
		trigger = "kind",
		category = "Custom",
		description = "Kind of binary when building",
		default = "shared",
		allowed = {
			{"exe", "Executable"},
			{"static", "Static library"},
			{"shared", "Shared library"},
		}
	})
	newoption({
		trigger = "disableintnj",
		category = "Custom",
		description = "Disable Integer NJ Network from popart"
	})
	newoption({
		trigger = "enablepbar",
		category = "Custom",
		description = "Enable the progressbar of Popart"
	})
	newoption({
		trigger = "includedirs",
		category = "Custom",
		description = "List of include directories separated by semicolons"
	})
	newoption({
		trigger = "libdirs",
		category = "Custom",
		description = "List of library directories separated by semicolons"
	})
	newoption({
		trigger = "target",
		category = "Custom",
		description = "The produced library is copied here"
	})
	newoption({
		trigger = "arch",
		category = "Custom",
		description = "Target architecture",
		default = "x86_64",
		allowed = {
			{"x86", "x86/x32, 32 bit architecture"},
			{"x86_64", "x86_64/x64, 64 bit architecture"},
			{"arm64", "arm64, 64 bit architecture"},
		}
	})
	newoption({
		trigger = "pythonlib",
		category = "Custom",
		description = "Python library to link against",
		default = "python3.11"
	})
	newoption({
		trigger = "nopython",
		category = "Custom",
		description = "Disable Python bindings"
	})


	project("popart_networks")
		filter("options:kind=exe")
			kind("ConsoleApp")
		filter("options:kind=static")
			kind("StaticLib")
		filter("options:kind=shared")
			kind("SharedLib")
		filter("options:*")
		language("C++")
		cppdialect("C++17")
		architecture(_OPTIONS["arch"])
		warnings("Extra")
		location("build")
		linkoptions({})

		includedirs({
			"src/itaxotools/_popart_networks/include",
			"src/popart/src",
		})
		files({
			"src/itaxotools/_popart_networks/src/*.cpp",
			--"popart/src/testgraphs.cpp"
		})
		links({
			"popart"
		})

		if _OPTIONS["includedirs"] then
			for path in string.gmatch(_OPTIONS["includedirs"], "[^;]+") do
			  includedirs { path }
			end
		end

		if _OPTIONS["libdirs"] then
			for path in string.gmatch(_OPTIONS["libdirs"], "[^;]+") do
			  libdirs { path }
			end
		end

		if _OPTIONS["target"] then
			filter({"not system:windows"})
				postbuildcommands {
					"{COPYFILE} %{cfg.buildtarget.relpath} " .. _OPTIONS["target"]
				}
			filter({"system:windows"})
				postbuildcommands {
					"{COPYFILE} $(TargetPath) " .. _OPTIONS["target"]
				}
			filter({})
		end

		filter({"options:disableintnj"})
			defines({"DISABLE_INTNJ"})
		filter({"not options:disableintnj"})
			links({"lpsolve55"})

		filter("not options:nopython")
			links(_OPTIONS["pythonlib"])
		filter("options:nopython")
			removefiles({
				"src/itaxotools/_popart_networks/src/python_wrapper.cpp",
			})

		filter({"not system:windows"})
			buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"comment",
				"catch-value",
				"sign-compare"
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")
		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")


	project("popart")
		kind("StaticLib")
		kind("StaticLib")
		language("C++")
		cppdialect("C++11")
		architecture(_OPTIONS["arch"])
		warnings("Extra")
		location("build")
		linkoptions({})

		includedirs({
			"src/popart/src/networks",
			"src/popart/src/tree",
			"src/popart/src/seqio",
		})
		files({
			"src/popart/src/networks/*.cpp",
			"src/popart/src/tree/*.cpp",
			"src/popart/src/seqio/*.cpp",
		})

		filter({"options:disableintnj"})
			removefiles({"src/popart/src/networks/IntNJ.cpp"})
		filter({"not options:disableintnj"})
			links({"lpsolve55"})

		filter({"not options:enablepbar"})
			defines({"DISABLE_PROGRESSBAR"})

		filter({"not system:windows"})
			--buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"sign-compare",
				"deprecated-copy",
				"mismatched-new-delete",
				"maybe-uninitialized",
				"char-subscripts",
				"misleading-indentation",
				"implicit-fallthrough",
				"unused-but-set-variable",
				"unused-result",
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")
		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")
