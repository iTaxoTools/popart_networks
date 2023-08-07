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
		trigger = "disablepbar",
		category = "Custom",
		description = "Disable the progressbar of Popart"
	})
	newoption({
		trigger = "nopython",
		category = "Custom",
		description = "Disable Python bindings"
	})
	newoption({
		trigger = "pythonversion",
		category = "Custom",
		description = "Python version to link against for non-Windows systems",
		default = "3.11"
	})
	newoption({
		trigger = "pythonpath",
		category = "Custom",
		description = "Python path"
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

		includedirs({
			"include",
			"popart/src",
		})
		filter({"system:not windows"})
			includedirs("/usr/include/python" .. _OPTIONS["pythonversion"])
		filter({})
		files({
			"src/*.cpp",
			--"popart/src/testgraphs.cpp"
		})
		filter({"not options:nopython", "system:windows"})
			removefiles({
				"src/python_wrapper.cpp",
			})
		filter({"options:disableintnj"})
			defines({"DISABLE_INTNJ"})
		filter({"not options:disableintnj"})
			links({"lpsolve55"})
		filter({})

		location("build")
		--targetdir("build/bin/${cfg.buildcfg}")
		--targetname("popart_networks")
		filter({})
		links({
			"popart"
		})
		if _OPTIONS["pythonpath"] then
			includedirs({_OPTIONS["pythonpath"] .. "/include"})
			filter({"system:windows"})
				libdirs(_OPTIONS["pythonpath"] .. "/libs")
			filter({})
		end
		filter({"not options:nopython", "system:windows"})
			links("python3")
		filter({"not options:nopython", "system:not windows"})
			links("python" .. _OPTIONS["pythonVersion"])
		filter({})
		--pic("On")
		linkoptions({})
		warnings("Extra")
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
		language("C++")
		--cppdialect("C++11")

		includedirs({
			"popart/src/networks",
			"popart/src/tree",
			"popart/src/seqio",
		})
		files({
			"popart/src/networks/*.cpp",
			"popart/src/tree/*.cpp",
			"popart/src/seqio/*.cpp",
		})

		location("build")
		filter({"not options:disableintnj"})
			links({"lpsolve55"})
		filter({})
		--pic("On")
		linkoptions({})
		warnings("Extra")
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
		filter({"options:disableintnj"})
			removefiles({"popart/src/networks/IntNJ.cpp"})
			defines({"DISABLE_INTNJ"})
		filter({"options:disablepbar"})
			defines({"DISABLE_PROGRESSBAR"})
		filter({})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")

		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")
